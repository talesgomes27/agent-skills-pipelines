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
SKILLS = set(json.loads((REPO / 'distribution/catalog.json').read_text(encoding='utf-8'))['skills'])
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
                self.assertIn(t['esperado'], ('deve', 'ambiguo_deve', 'nao_deve'))
                self.assertTrue(t['prompt'].strip())


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


@unittest.skipIf(yaml is None, 'PyYAML ausente')
class ResultFormat(unittest.TestCase):
    def test_results_match_scenarios(self):
        self.check_results(EVALS / 'results')

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
                    continue
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
                self.assertLessEqual({s for s in data['skills_carregadas'] if ':' not in s}, SKILLS)
                self.assertIs(type(data['paradas']), int)
                self.assertIs(type(data['contexto_lido']['caracteres']), int)
                self.assertIsInstance(data['contexto_lido']['arquivos'], list)
                known = {c['id'] for c in scenario['checkpoints']}
                for c in data['checkpoints']:
                    self.assertIn(c['id'], known)
                    self.assertIn(c['resultado'], ('passou', 'falhou', 'indeterminado'))
                    self.assertTrue(c['evidencia'].strip())


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
                dup.append((str(seen[key].relative_to(root)), str(path.relative_to(root)), c['id']))
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
            log.write_text('lixo\n' + uso('asp:audit-and-refactoring-pipeline') + '\n', encoding='utf-8')
            self.assertEqual(ex.gatilho(log, 'audit-and-refactoring-pipeline'), 'ativou')
            self.assertEqual(ex.gatilho(log, 'execution-pipeline'), 'outra')
            log.write_text('', encoding='utf-8')
            self.assertEqual(ex.gatilho(log, 'execution-pipeline'), 'nao_ativou')


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
