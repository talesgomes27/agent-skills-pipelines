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
                self.assertIn(s['modo'], ('assistido', 'continuo'))
                if 'esforco_esperado' in s:
                    self.assertIn(s['esforco_esperado'], ('leve', 'padrao', 'rigoroso'))
                if 'paradas_esperadas' in s:
                    self.assertIs(type(s['paradas_esperadas']), int)
                if 'fixture' in s:
                    self.assertTrue((EVALS / s['fixture']).is_dir())
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
class ResultFormat(unittest.TestCase):
    def test_results_match_scenarios(self):
        found = scenarios()
        for path in sorted((EVALS / 'results').rglob('*.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            with self.subTest(resultado=str(path.relative_to(EVALS))):
                self.assertEqual(data['versao'], path.parent.name)
                self.assertRegex(data['versao'], r'^\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?$')
                self.assertIn(data['nivel'], ('leitura', 'execucao'))
                self.assertTrue(data['host'] and data['modelo'])
                datetime.date.fromisoformat(data['data'])
                if path.name.startswith('triggers-'):
                    trig = {t['id'] for t in yaml.safe_load((EVALS / 'triggers.yaml').read_text(encoding='utf-8'))}
                    for r in data['resultados']:
                        self.assertIn(r['id'], trig)
                        self.assertIn(r['observado'], ('ativou', 'nao_ativou', 'outra'))
                    continue
                self.assertEqual(data['cenario'], path.stem)
                scenario = found[data['cenario']]
                self.assertIsInstance(data['skills_carregadas'], list)
                self.assertLessEqual(set(data['skills_carregadas']), SKILLS)
                self.assertIs(type(data['paradas']), int)
                self.assertIs(type(data['contexto_lido']['caracteres']), int)
                self.assertIsInstance(data['contexto_lido']['arquivos'], list)
                known = {c['id'] for c in scenario['checkpoints']}
                for c in data['checkpoints']:
                    self.assertIn(c['id'], known)
                    self.assertIn(c['resultado'], ('passou', 'falhou', 'indeterminado'))
                    self.assertTrue(c['evidencia'].strip())


if __name__ == '__main__':
    unittest.main()
