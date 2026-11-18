import contextlib
import datetime
import json
import re
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO = Path(__file__).resolve().parents[1]
EVALS = REPO / 'evals'
MODOS = ('por-efeito', 'assistido', 'continuo')
CATALOG = json.loads((REPO / 'distribution/catalog.json').read_text(encoding='utf-8'))
SKILLS = set(CATALOG['skills'])
# resultados de antes da 5.0.0 guardam os nomes antigos das skills renomeadas
SKILLS_ANTES_DA_5 = SKILLS | set(CATALOG.get('renamed', {}))


def skills_validas(versao):
    return SKILLS_ANTES_DA_5 if int(versao.split('.')[0]) < 5 else SKILLS


ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def scenarios():
    return {p.stem: yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted((EVALS / 'scenarios').glob('*.yaml'))}


@unittest.skipIf(yaml is None, 'PyYAML ausente')
class ScenarioFormat(unittest.TestCase):
    def test_scenarios_are_well_formed(self):
        found = scenarios()
        self.assertTrue(found)
        for stem, s in found.items():
            with self.subTest(cenario=stem):
                self.assertEqual(s['id'], stem)
                self.assertRegex(s['id'], ID)
                self.assertIsInstance(s['pedido'], str)
                self.assertTrue(s['pedido'].strip())
                self.assertIsInstance(s['skills_esperadas'], list)
                self.assertTrue(s['skills_esperadas'])
                if 'arquetipo_esperado' in s:
                    self.assertIn(s['arquetipo_esperado'].get('principal'), ('A', 'B', 'C'))
                    self.assertLessEqual(set(s['arquetipo_esperado']), {'principal', 'secundario'})
                self.assertLessEqual(set(s['skills_esperadas']), SKILLS)
                self.assertIn(s['modo'], MODOS)
                if 'esforco_esperado' in s:
                    self.assertIn(s['esforco_esperado'], ('leve', 'padrao', 'rigoroso'))
                if 'paradas_esperadas' in s:
                    esperadas = s['paradas_esperadas']
                    if isinstance(esperadas, dict):
                        self.assertTrue(esperadas)
                        self.assertLessEqual(set(esperadas), set(MODOS))
                        self.assertTrue(all(type(v) is int for v in esperadas.values()))
                    else:
                        self.assertIs(type(esperadas), int)
                if 'fixture' in s:
                    self.assertTrue((EVALS / s['fixture']).is_dir())
                if 'aceite_simulado' in s:
                    self.assertIsInstance(s['aceite_simulado'], str)
                    self.assertTrue(s['aceite_simulado'].strip())
                ids = [c['id'] for c in s['checkpoints']]
                self.assertEqual(len(ids), len(set(ids)))
                tipos = {c['tipo'] for c in s['checkpoints']}
                self.assertEqual(tipos, {'deve', 'nao_deve'})
                for c in s['checkpoints']:
                    self.assertRegex(c['id'], ID)
                    self.assertIsInstance(c['descricao'], str)
                    self.assertTrue(c['descricao'].strip())

    def test_triggers_are_well_formed(self):
        path = EVALS / 'triggers.yaml'
        if not path.exists():
            self.skipTest('sem triggers.yaml')
        items = yaml.safe_load(path.read_text(encoding='utf-8'))
        ids = [t['id'] for t in items]
        self.assertEqual(len(ids), len(set(ids)))
        for t in items:
            with self.subTest(gatilho=t['id']):
                self.assertIn(t['skill'], SKILLS)
                self.assertIn(t['esperado'], ('deve', 'ambiguo_deve', 'nao_deve', 'opcional'))
                self.assertTrue(t['prompt'].strip())
                if 'fixture' in t:
                    self.assertTrue(t['fixture'].startswith('fixtures/'))
                    self.assertTrue(any(p.is_file() for p in (EVALS / t['fixture']).rglob('*')))
                self.assertLessEqual(set(t), {'id', 'skill', 'esperado', 'prompt', 'fixture'})


@unittest.skipIf(yaml is None, 'PyYAML ausente')
class MatrixAndReport(unittest.TestCase):
    def test_matrix_is_well_formed(self):
        m = yaml.safe_load((EVALS / 'matrix.yaml').read_text(encoding='utf-8'))
        self.assertTrue(m['combinacoes'])
        for c in m['combinacoes']:
            self.assertTrue(c['host'] and c['modelo'])
        self.assertLessEqual(set(m['niveis']), {'leitura', 'execucao'})

    def test_report_reads_nao_deve_checkpoints(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('report', EVALS / 'report.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        expected = {k: {c['id'] for c in s['checkpoints'] if c['tipo'] == 'nao_deve'} for k, s in scenarios().items()}
        self.assertEqual(mod.nao_deve_ids(), expected)
        mod.rows()

    def test_report_separates_destinations_of_the_same_host(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location('report', EVALS / 'report.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        base = {'cenario': 'x', 'versao': '9.0.0', 'nivel': 'execucao', 'host': 'claude-code', 'modelo': 'm', 'data': '2026-11-08', 'checkpoints': []}
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / '9.0.0/execucao/claude-code-instalador').mkdir(parents=True)
            (root / '9.0.0/execucao/x.json').write_text(json.dumps(base), encoding='utf-8')
            (root / '9.0.0/execucao/claude-code-instalador/x.json').write_text(json.dumps(dict(base, destino='claude-code-instalador')), encoding='utf-8')
            keys = set(mod.rows(root=root))
        self.assertEqual({k[4] for k in keys}, {'', 'claude-code-instalador'})

    def test_report_pairs_each_destination_with_the_no_skill_arm(self):
        import tempfile
        mod = self._report()
        base = {'cenario': 'x', 'versao': '9.0.0', 'nivel': 'execucao', 'modo': 'por-efeito', 'host': 'claude-code', 'modelo': 'm', 'data': '2026-11-17'}
        cp = lambda **r: [{'id': i, 'resultado': v, 'evidencia': i} for i, v in r.items()]
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / '9.0.0/execucao/sem-skill').mkdir(parents=True)
            (root / '9.0.0/execucao/x.json').write_text(json.dumps(dict(base, skills_carregadas=['s'], checkpoints=cp(a='passou', b='passou', c='falhou'))), encoding='utf-8')
            (root / '9.0.0/execucao/sem-skill/x.json').write_text(json.dumps(dict(base, destino='sem-skill', checkpoints=cp(a='passou', b='falhou'))), encoding='utf-8')
            (root / '9.0.0/execucao/y.json').write_text(json.dumps(dict(base, cenario='y', checkpoints=cp(a='passou'))), encoding='utf-8')
            rows = mod.delta_rows(root=root)
        # y não tem o braço sem a skill; c não foi julgado sem a skill e fica fora da comparação
        self.assertEqual(rows, [{'versao': '9.0.0', 'nivel': 'execucao', 'modo': 'por-efeito', 'cenario': 'x', 'destino': '',
                                 'com': 2, 'sem': 1, 'comparados': 2, 'nos_dois': ['a'], 'skills': ['s']}])

    def _report(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('report', EVALS / 'report.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_report_situation_separates_failed_from_undetermined(self):
        import tempfile
        mod = self._report()
        proibidos = {'x': {'p'}}

        def situacao(*checkpoints):
            d = {'cenario': 'x', 'versao': '9.0.0', 'nivel': 'execucao', 'host': 'h', 'modelo': 'm', 'data': '2026-11-14',
                 'checkpoints': [{'id': i, 'resultado': r} for i, r in checkpoints]}
            with tempfile.TemporaryDirectory() as t:
                (Path(t) / '9.0.0/execucao').mkdir(parents=True)
                (Path(t) / '9.0.0/execucao/x.json').write_text(json.dumps(d), encoding='utf-8')
                (a,) = mod.rows(root=Path(t), proibidos=proibidos).values()
            return mod.situacao(a), a
        self.assertEqual(situacao(('p', 'falhou'), ('d', 'passou'))[0], 'não recomendada')
        self.assertEqual(situacao(('p', 'indeterminado'), ('d', 'passou'))[0], 'sem evidência')
        self.assertEqual(situacao(('d', 'passou'))[0], 'sem evidência')  # nenhum nao_deve julgado
        self.assertEqual(situacao()[0], 'sem evidência')
        self.assertEqual(situacao(('p', 'passou'), ('d', 'falhou'), ('e', 'passou'))[0], 'parcial')
        s, a = situacao(('p', 'passou'), ('d', 'passou'), ('e', 'indeterminado'))
        self.assertEqual(s, 'ok')
        self.assertEqual((a['deve']['passou'], a['deve']['indeterminado'], a['deve']['falhou']), (1, 1, 0))

    def test_report_counts_triggers(self):
        import tempfile
        mod = self._report()
        gatilhos = {'a': 'deve', 'b': 'ambiguo_deve', 'c': 'nao_deve', 'd': 'nao_deve', 'o': 'opcional'}
        d = {'versao': '9.0.0', 'nivel': 'execucao', 'host': 'claude-code', 'modelo': 'm', 'data': '2026-11-14',
             'resultados': [{'id': 'a', 'observado': 'nao_ativou'}, {'id': 'b', 'observado': 'ativou', 'amostras': ['ativou', 'nao_ativou']},
                            {'id': 'c', 'observado': 'outra'}, {'id': 'd', 'observado': 'ativou'},
                            {'id': 'saiu-do-yaml', 'observado': 'ativou'}, {'id': 'o', 'observado': 'nao_ativou'}]}
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / '9.0.0/execucao').mkdir(parents=True)
            (Path(t) / '9.0.0/execucao/triggers-claude-code.json').write_text(json.dumps(d), encoding='utf-8')
            (Path(t) / '9.0.0/execucao/triggers-claude-code-instalador.json').write_text(
                json.dumps(dict(d, destino='claude-code-instalador', resultados=d['resultados'][1:3])), encoding='utf-8')
            r = mod.trigger_rows(root=Path(t), gatilhos=gatilhos)
        marketplace = r[('9.0.0', 'execucao', 'claude-code', '', 'm')]
        self.assertEqual((marketplace['certos'], marketplace['total'], marketplace['erros_deve'], marketplace['ativou_nao_deve'],
                          marketplace['ignorados']), (1, 4, 2, 1, 1))
        instalador = r[('9.0.0', 'execucao', 'claude-code', 'claude-code-instalador', 'm')]
        # b foi gravado como ativou, mas uma amostra não ativou: pelas amostras, não é certo
        self.assertEqual((instalador['certos'], instalador['total']), (1, 2))
        # os outros não têm amostras e valem pelo observado
        self.assertEqual((marketplace['amostras_certas'], marketplace['amostras']), (2, 5))
        self.assertEqual((instalador['amostras_certas'], instalador['amostras']), (2, 3))

    def test_report_wilson_interval(self):
        mod = self._report()
        self.assertEqual(mod.wilson(0, 0), '—')
        self.assertEqual(mod.wilson(3, 3), '44 a 100%')
        self.assertEqual(mod.wilson(5, 10), '24 a 76%')

    def test_report_cost_shows_coverage(self):
        mod = self._report()
        self.assertEqual(mod.custo([]), '—')
        self.assertEqual(mod.custo([None]), '—')
        self.assertEqual(mod.custo([0.25, 0.5]), '0.75')
        self.assertEqual(mod.custo([0.25, None]), '0.25 (1 de 2)')

    def test_report_reads_triggers_without_pyyaml(self):
        mod = self._report()
        real = mod.gatilhos_esperados()
        texto = (EVALS / 'triggers.yaml').read_text(encoding='utf-8')
        self.assertEqual(mod.gatilhos_esperados(texto_sem_yaml=texto), real)


@unittest.skipIf(yaml is None, 'PyYAML ausente')
class ResultFormat(unittest.TestCase):
    def test_results_match_scenarios(self):
        self.check_results(EVALS / 'results')

    def test_old_skill_names_only_before_5(self):
        for old, new in CATALOG['renamed'].items():
            self.assertIn(old, skills_validas('4.3.2'))
            self.assertNotIn(old, skills_validas('5.0.0'))
            self.assertIn(new, skills_validas('5.0.0'))

    def test_evidence_is_not_copied_between_runs(self):
        import collections
        por_versao = collections.Counter(d[0].split('/')[0] for d in copied_evidence(EVALS / 'results'))
        self.assertEqual(dict(por_versao), ANTES_DA_REGRA)

    def test_copied_evidence_is_detected(self):
        import tempfile
        ev = 'Texto final: o agente pediu o A2 do deploy antes de publicar no servidor.'
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for sub in ('9.0.0/execucao', '9.0.0/execucao/claude-code-instalador'):
                (root / sub).mkdir(parents=True, exist_ok=True)
                (root / sub / 'x.json').write_text(json.dumps({'cenario': 'x', 'versao': '9.0.0', 'checkpoints': [{'id': 'a', 'evidencia': ev}]}), encoding='utf-8')
            self.assertEqual(len(copied_evidence(root)), 1)
            # evidência curta, evidência diferente e resultado de gatilhos não contam
            (root / '9.0.0/execucao/claude-code-instalador/x.json').write_text(json.dumps({'cenario': 'x', 'versao': '9.0.0', 'checkpoints': [
                {'id': 'a', 'evidencia': ev + ' Outra.'}, {'id': 'b', 'evidencia': 'curta'}]}), encoding='utf-8')
            (root / '9.0.0/execucao/x2.json').write_text(json.dumps({'cenario': 'x', 'versao': '9.0.0', 'checkpoints': [{'id': 'b', 'evidencia': 'curta'}]}), encoding='utf-8')
            (root / '9.0.0/execucao/triggers-claude-code.json').write_text(json.dumps({'versao': '9.0.0', 'resultados': []}), encoding='utf-8')
            self.assertEqual(copied_evidence(root), [])

    def test_destination_subfolder_and_trigger_name(self):
        import tempfile
        sid = sorted(scenarios())[0]
        base = {'cenario': sid, 'versao': '9.0.0', 'nivel': 'execucao', 'host': 'claude-code', 'modelo': 'm', 'data': '2026-11-08',
                'skills_carregadas': [], 'paradas': 0, 'contexto_lido': {'caracteres': 0, 'arquivos': []}, 'checkpoints': [], 'destino': 'claude-code-instalador'}
        trig = {'versao': '9.0.0', 'nivel': 'execucao', 'host': 'claude-code', 'modelo': 'm', 'data': '2026-11-08', 'resultados': [], 'destino': 'claude-code-instalador'}
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / 'results'
            (root / '9.0.0/execucao/claude-code-instalador').mkdir(parents=True)
            (root / '9.0.0/execucao/claude-code-instalador' / (sid + '.json')).write_text(json.dumps(base), encoding='utf-8')
            (root / '9.0.0/execucao/triggers-claude-code-instalador.json').write_text(json.dumps(trig), encoding='utf-8')
            self.check_results(root)
            (root / '9.0.0/execucao/outra').mkdir()
            (root / '9.0.0/execucao/outra' / (sid + '.json')).write_text(json.dumps(base), encoding='utf-8')
            with self.assertRaises(AssertionError):
                self.check_results(root, sub=False)

    def check_results(self, root, sub=True):
        found = scenarios()
        for path in sorted(root.rglob('*.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            with (self.subTest(resultado=str(path.relative_to(root))) if sub else contextlib.nullcontext()):
                # <versão>/<nível>/<arquivo>, ou <versão>/<nível>/<destino>/<arquivo> com o campo destino
                nivel_dir = path.parent
                if not path.name.startswith('triggers-') and (path.parent.name not in ('leitura', 'execucao') or 'destino' in data):
                    self.assertEqual(data.get('destino'), path.parent.name)
                    nivel_dir = path.parent.parent
                self.assertEqual(nivel_dir.name, data['nivel'])
                self.assertEqual(data['versao'], nivel_dir.parent.name)
                self.assertRegex(data['versao'], r'^\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?$')
                self.assertIn(data['nivel'], ('leitura', 'execucao'))
                self.assertTrue(data['host'] and data['modelo'])
                datetime.date.fromisoformat(data['data'])
                if path.name.startswith('triggers-'):
                    self.assertEqual(path.stem[len('triggers-'):], data.get('destino', data['host']))
                    trig = {t['id'] for t in yaml.safe_load((EVALS / 'triggers.yaml').read_text(encoding='utf-8'))}
                    for r in data['resultados']:
                        self.assertIn(r['id'], trig)
                        self.assertIn(r['observado'], ('ativou', 'nao_ativou', 'outra'))
                        self.assertLessEqual(set(r.get('amostras', [])), {'ativou', 'nao_ativou', 'outra'})
                    self.check_metricas(data.get('metricas'))
                    continue
                self.check_metricas(data.get('metricas'))
                # <id>.json no modo padrão da versão; <id>--<modo>.json nos outros
                stem, _, modo = path.stem.partition('--')
                self.assertEqual(data['cenario'], stem)
                if modo:
                    self.assertEqual(data.get('modo'), modo)
                if 'modo' in data:
                    self.assertIn(data['modo'], MODOS)
                scenario = found[data['cenario']]
                self.assertIsInstance(data['skills_carregadas'], list)
                # skills de outros plugins vêm com prefixo, como superpowers:brainstorming
                self.assertLessEqual({s for s in data['skills_carregadas'] if ':' not in s}, skills_validas(data['versao']))
                self.assertIs(type(data['paradas']), int)
                self.assertIs(type(data['contexto_lido']['caracteres']), int)
                self.assertIsInstance(data['contexto_lido']['arquivos'], list)
                known = {c['id'] for c in scenario['checkpoints']}
                for c in data['checkpoints']:
                    self.assertIn(c['id'], known)
                    self.assertIn(c['resultado'], ('passou', 'falhou', 'indeterminado'))
                    self.assertTrue(c['evidencia'].strip())

    def check_metricas(self, m):
        # opcional; um valor que o host não deu fica null, nunca 0
        if m is None:
            return
        self.assertLessEqual(set(m), {'custo_usd', 'turnos', 'duracao_ms', 'tokens', 'sem_custo'})
        for k in ('custo_usd', 'turnos', 'duracao_ms', 'sem_custo'):
            self.assertTrue(m.get(k) is None or (isinstance(m[k], (int, float)) and m[k] >= 0), k)
        if m.get('tokens') is not None:
            self.assertEqual(set(m['tokens']), {'entrada', 'saida', 'cache_leitura', 'cache_escrita'})


# resultados julgados antes da regra de evidência própria (4.2.0), sem os registros das execuções para rejulgar:
# quantas duplicatas cada versão tem; uma nova muda a contagem e falha
ANTES_DA_REGRA = {'4.0.0-dev': 116, '4.0.0': 229, '4.0.1': 11, '4.0.2': 12}


def copied_evidence(root):
    # a mesma evidência inteira em dois resultados do mesmo cenário e versão indica juiz que copiou entre execuções
    seen, dup = {}, []
    for path in sorted(root.rglob('*.json')):
        if path.name.startswith('triggers-'):
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        for c in data.get('checkpoints', []):
            ev = ' '.join(c.get('evidencia', '').split())
            if len(ev) <= 40:
                continue
            key = (data['versao'], data['cenario'], ev)
            if key in seen and seen[key] != path:
                dup.append((seen[key].relative_to(root).as_posix(), path.relative_to(root).as_posix(), c["id"]))
            seen.setdefault(key, path)
    return dup


class Harness(unittest.TestCase):
    def test_trigger_classification(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        uso = lambda nome: json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Skill', 'input': {'skill': nome}}]}})
        with tempfile.TemporaryDirectory() as t:
            log = Path(t) / 'log.jsonl'
            log.write_text('lixo\n' + uso('audit-and-refactoring-pipeline:audit-and-refactoring-pipeline') + '\n', encoding='utf-8')
            self.assertEqual(ex.gatilho(log, 'audit-and-refactoring-pipeline'), 'ativou')
            self.assertEqual(ex.gatilho(log, 'implementation-pipeline'), 'outra')
            log.write_text('', encoding='utf-8')
            self.assertEqual(ex.gatilho(log, 'implementation-pipeline'), 'nao_ativou')

    def test_plugin_mirrors_marketplace(self):
        import contextlib
        import importlib.util
        import io
        import tempfile
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        mkt = json.loads((REPO / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))['plugins']
        with tempfile.TemporaryDirectory() as t, contextlib.redirect_stdout(io.StringIO()):
            ex.plugin(t)
            raiz = Path(t) / 'plugins'
            self.assertEqual(sorted(d.name for d in raiz.iterdir()), sorted(p['name'] for p in mkt if not p.get('dependencies')))
            for p in mkt:
                for s in p.get('skills', []):
                    self.assertTrue((raiz / p['name'] / 'skills' / Path(s).name / 'SKILL.md').is_file(), s)
                    nome = json.loads((raiz / p['name'] / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))['name']
                    self.assertEqual(nome, p['name'])
                for a in p.get('agents', []):
                    self.assertTrue((raiz / p['name'] / 'agents' / Path(a).name).is_file(), a)
            self.assertTrue((raiz / 'pipeline-guardrails' / 'effects.json').is_file())

    def test_lote_no_skill_arm_skips_triggers(self):
        import contextlib
        import importlib.util
        import io
        import tempfile
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        with tempfile.TemporaryDirectory() as t, contextlib.redirect_stdout(io.StringIO()) as out:
            ex.lote(t, gatilhos=['release-and-ops-pipeline-incidente-1'], destinos=['sem-skill'])
            self.assertFalse((Path(t) / 'sem-skill').exists())
        self.assertIn('0 execuções', out.getvalue())
        with tempfile.TemporaryDirectory() as t, self.assertRaises(SystemExit):
            ex.lote(t, destinos=['outro'])

    def test_estado_lists_files_commands_and_git_effects(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        uso = lambda i, cmd: {'type': 'tool_use', 'id': i, 'name': 'Bash', 'input': {'command': cmd}}
        res = lambda i, txt, erro=False: {'type': 'tool_result', 'tool_use_id': i, 'content': txt, 'is_error': erro}
        with tempfile.TemporaryDirectory() as t:
            exe = Path(t)
            ex.preparar(exe, 'p', 'fixtures/gatilho-retomada')
            (exe / 'meta.json').write_text(json.dumps({'fixture': 'fixtures/gatilho-retomada'}))
            (exe / 'proj/app.py').write_text('mudou')
            (exe / 'proj/user-notes.txt').unlink()
            (exe / 'proj/novo.md').write_text('x')
            (exe / 'proj/.claude/skills').mkdir(parents=True)
            (exe / 'proj/.claude/skills/s.md').write_text('do harness')
            linhas = [{'type': 'assistant', 'message': {'content': [uso('a', 'python -m pytest -q'),
                       {'type': 'tool_use', 'id': 's', 'name': 'Skill', 'input': {'skill': 'plug:implementation-pipeline'}}]}},
                      {'type': 'user', 'message': {'content': [res('a', [{'type': 'text', 'text': '..\n1 passed in 0.01s\n'}])]}}]
            (exe / 'log.jsonl').write_text('\n'.join(map(json.dumps, linhas)))
            (exe / 'log2.jsonl').write_text(json.dumps({'type': 'assistant', 'message': {'content': [uso('b', 'git push origin main')]}}) + '\n' +
                                            json.dumps({'type': 'user', 'message': {'content': [res('b', 'negado', True)]}}))
            e = ex.estado(exe)
        self.assertEqual((e['criados'], e['apagados'], e['alterados']), (['novo.md'], ['user-notes.txt'], ['app.py']))
        self.assertEqual(e['skills'], ['implementation-pipeline'])
        self.assertEqual(e['comandos'], [
            {'turno': 1, 'comando': 'python -m pytest -q', 'erro': False, 'ultima_linha': '1 passed in 0.01s'},
            {'turno': 2, 'comando': 'git push origin main', 'erro': True, 'ultima_linha': 'negado'}])
        self.assertEqual([c['comando'] for c in e['git_efeito']], ['git push origin main'])
        for cmd in ('git -C x push', 'git -c a=b commit -m x', 'cat > a <<EOF\n' + 'x' * 400 + '\nEOF\n&& git commit -am x',
                    'git branch -D velha', 'gh pr merge 3'):
            self.assertTrue(ex.GIT_EFEITO.search(cmd), cmd)
        for cmd in ('git commit-tree abc', 'git push-x', 'git status', 'git diff HEAD'):
            self.assertFalse(ex.GIT_EFEITO.search(cmd), cmd)
        with tempfile.TemporaryDirectory() as t, self.assertRaises(SystemExit):
            ex.estado(t, 'fixtures/nao-existe')
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / 'meta.json').write_text(json.dumps({'tipo': 'cenario', 'id': 'retomada-base-mudou-plano-vale'}))
            self.assertEqual(ex.estado(t)['fixture'], 'fixtures/gatilho-retomada')  # meta.json antigo, sem a chave
            (Path(t) / 'proj').mkdir()
            (Path(t) / 'proj/a.txt').write_text('x')
            self.assertEqual(ex.estado(t, '')['criados'], ['a.txt'])  # proj que começou vazio

    def test_contar_reads_lote_layout(self):
        import contextlib
        import importlib.util
        import io
        import tempfile
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        uso = json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'release-and-ops-pipeline:release-and-ops-pipeline'}}]}})
        with tempfile.TemporaryDirectory() as t:
            for n, log, done in ((1, uso, True), (2, '', True), (3, uso, False)):
                exe = Path(t) / 'claude-code' / f'gatilho-release-and-ops-pipeline-incidente-1-{n}'
                exe.mkdir(parents=True)
                (exe / 'meta.json').write_text(json.dumps({'tipo': 'gatilho', 'id': 'release-and-ops-pipeline-incidente-1', 'destino': 'claude-code', 'amostra': n}))
                (exe / 'log.jsonl').write_text(log + '\n', encoding='utf-8')
                if done:
                    (exe / 'done').write_text('0')
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                ex.contar(t, '4.3.0')
            texto = out.getvalue()
            self.assertIn('1/2 certos (ati nao)', texto)
            self.assertIn('1 execuções sem done', texto)
            self.assertIn('| 4.3.0: ativou', texto)  # o --contra lê o resultado publicado
            (Path(t) / 'claude-code' / 'quebrada').mkdir()
            (Path(t) / 'claude-code' / 'quebrada' / 'meta.json').write_text('{')
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                ex.contar(t, '4.3.0')
            self.assertIn('1 pastas com meta.json inválido', out.getvalue())

    def _ex(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        return ex

    def test_metricas_sums_both_turns_and_keeps_missing_as_none(self):
        import tempfile
        ex = self._ex()
        res = lambda **k: json.dumps(dict({'type': 'result', 'subtype': 'success'}, **k))
        uso = {'input_tokens': 6, 'output_tokens': 100, 'cache_read_input_tokens': 900, 'cache_creation_input_tokens': 50}
        with tempfile.TemporaryDirectory() as t:
            exe = Path(t)
            (exe / 'log.jsonl').write_text(res(total_cost_usd=0.25, num_turns=5, duration_ms=1000, usage=uso) + '\n', encoding='utf-8')
            (exe / 'log2.jsonl').write_text('lixo\n' + res(total_cost_usd=0.5, num_turns=2, duration_ms=500, usage=uso) + '\n', encoding='utf-8')
            m = ex.metricas(exe)
            self.assertEqual((m['custo_usd'], m['turnos'], m['duracao_ms']), (0.75, 7, 1500))
            self.assertEqual(m['tokens'], {'entrada': 12, 'saida': 200, 'cache_leitura': 1800, 'cache_escrita': 100})
            (exe / 'log2.jsonl').unlink()
            (exe / 'log.jsonl').write_text(res(num_turns=3) + '\n', encoding='utf-8')
            m = ex.metricas(exe)
            self.assertEqual((m['custo_usd'], m['turnos'], m['duracao_ms'], m['tokens']), (None, 3, None, None))  # ausente não vira 0
            (exe / 'log.jsonl').write_text('', encoding='utf-8')
            self.assertEqual(ex.metricas(exe), {'custo_usd': None, 'turnos': None, 'duracao_ms': None, 'tokens': None})

    def test_contar_json_keeps_samples(self):
        import contextlib
        import io
        import tempfile
        ex = self._ex()
        uso = json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'release-and-ops-pipeline:release-and-ops-pipeline'}}]}})
        fim = json.dumps({'type': 'result', 'subtype': 'success', 'total_cost_usd': 0.1, 'num_turns': 2, 'duration_ms': 10})
        with tempfile.TemporaryDirectory() as t:
            for n, log in ((1, uso + '\n' + fim), (2, fim), (3, uso)):
                exe = Path(t) / 'claude-code' / f'gatilho-release-and-ops-pipeline-incidente-1-{n}'
                exe.mkdir(parents=True)
                (exe / 'meta.json').write_text(json.dumps({'tipo': 'gatilho', 'id': 'release-and-ops-pipeline-incidente-1', 'destino': 'claude-code', 'amostra': n}))
                (exe / 'log.jsonl').write_text(log + '\n', encoding='utf-8')
                (exe / 'done').write_text('0')
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                ex.contar(t, json_saida=True)
            d = json.loads(out.getvalue())['claude-code']
        (r,) = d['resultados']
        # uma amostra errada basta para o observado ser o erro, como no "certos em todas as amostras"
        self.assertEqual(r, {'id': 'release-and-ops-pipeline-incidente-1', 'observado': 'nao_ativou', 'amostras': ['ativou', 'nao_ativou', 'ativou']})
        self.assertEqual(d['metricas'], {'custo_usd': 0.2, 'turnos': 4, 'duracao_ms': 20, 'sem_custo': 1})

    def test_api_error_does_not_mark_done(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location('execucao', REPO / '.claude/skills/cenarios/scripts/execucao.py')
        ex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex)
        # o formato real do evento result quando a conta atinge o limite de uso
        limite = {'type': 'result', 'subtype': 'success', 'is_error': True, 'api_error_status': 429, 'api_error': 'usage_limit_reached', 'session_id': 's'}
        ok = {'type': 'result', 'subtype': 'success', 'is_error': False, 'api_error_status': None, 'session_id': 's'}
        with tempfile.TemporaryDirectory() as t:
            exe = Path(t) / 'e'
            ex.preparar(exe, 'pedido')
            for evento, marcador in ((limite, 'erro_api'), (ok, 'done')):
                ex._claude = lambda proj, texto, log, *a, ev=evento: (Path(log).write_text(json.dumps(ev) + '\n', encoding='utf-8'), 0)[1]
                ex.rodar(exe, 'claude-code', plugin_dir=t)
                self.assertTrue((exe / marcador).exists())
            self.assertFalse((exe / 'erro_api').exists())


@unittest.skipIf(yaml is None, 'PyYAML ausente')
class IssueForm(unittest.TestCase):
    def test_skill_errou_lists_every_skill(self):
        form = yaml.safe_load((REPO / '.github/ISSUE_TEMPLATE/skill-errou.yml').read_text(encoding='utf-8'))
        fields = [b for b in form['body'] if b.get('id') == 'skill']
        self.assertEqual(len(fields), 1)
        options = fields[0]['attributes']['options']
        self.assertLessEqual(SKILLS, set(options))


if __name__ == '__main__':
    unittest.main()
