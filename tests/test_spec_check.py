import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('spec_check', REPO / 'pre-code-pipeline/scripts/spec_check.py')
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

SPEC = '''# Spec

## Requisitos
### R-001 Filtro
- Critério: Dado o filtro, Quando atualiza, Então o total bate.
- Estado: verificado
- Evidência: tests/test_filtro.py::test_r001

### R-002 Exportar
- Critério: Dado a seleção, Quando exporta, Então o CSV tem as linhas.
- Estado: aprovado

## Questões abertas
### Q-001 Quem recebe o alerta?
'''
PLAN = '''# Plano
### T-001 Filtro
- Requisitos: R-001
### T-002 Exportar
- Requisitos: R-002
'''


def run(root, *args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = sc.main(['--root', str(root)] + list(args))
    return code, out.getvalue() + err.getvalue()


class Base(unittest.TestCase):
    def tmp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        return Path(t.name)

    def write(self, root, files):
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding='utf-8')
        return root


class Native(Base):
    def project(self, spec=SPEC, plan=PLAN, evidence=True):
        files = {'docs/spec.md': spec}
        if plan is not None:
            files['docs/plan.md'] = plan
        if evidence:
            files['tests/test_filtro.py'] = ''
        return self.write(self.tmp(), files)

    def test_clean_spec_lists_open_questions(self):
        code, out = run(self.project())
        self.assertEqual(code, 0, out)
        self.assertIn('questão aberta: Q-001', out)

    def test_missing_evidence_file(self):
        code, out = run(self.project(evidence=False))
        self.assertEqual(code, 1)
        self.assertIn('R-001: evidência cita arquivo que não existe', out)

    def test_verified_without_evidence(self):
        code, out = run(self.project(spec=SPEC.replace('- Evidência: tests/test_filtro.py::test_r001\n', '')))
        self.assertEqual(code, 1)
        self.assertIn('R-001: verificado sem evidência', out)

    def test_approved_without_criterion_and_duplicate_and_bad_id(self):
        bad = SPEC.replace('- Critério: Dado a seleção, Quando exporta, Então o CSV tem as linhas.\n', '') + '### R-001 De novo\n- Estado: proposto\n### R-12 Curto\n### RF-003 Outro\n'
        code, out = run(self.project(spec=bad))
        self.assertEqual(code, 1)
        for msg in ('R-002: requisito aprovado sem critério', 'R-001: ID repetido', 'R-12: ID fora do padrão', 'RF-003: ID fora do padrão'):
            self.assertIn(msg, out)

    def test_state_is_validated_and_backticks_stripped(self):
        spec = SPEC.replace('- Estado: aprovado', '- Estado: `aprovado`') + '### R-003 Digitado errado\n- Critério: x\n- Estado: aprovdo\n### R-004 Sem estado\n'
        code, out = run(self.project(spec=spec, plan=PLAN + '### T-003 X\n- Requisitos: R-003, R-004\n'))
        self.assertEqual(code, 1)
        self.assertIn('R-003: estado ausente ou fora da lista', out)
        self.assertIn('R-004: estado ausente ou fora da lista', out)
        self.assertNotIn('R-002: estado', out)

    def test_fields_without_bullet_subheadings_and_continuation(self):
        spec = """### R-001 Filtro
#### Detalhe
Critério:
  Dado o filtro, Quando atualiza,
  Então o total bate.
Estado: aprovado
"""
        code, out = run(self.project(spec=spec, plan='### T-001 Filtro\nRequisitos: R-001\n'))
        self.assertEqual(code, 0, out)

    def test_evidence_ignores_urls_and_cell_anchors(self):
        spec = """### R-001 Total
- Critério: x
- Estado: verificado
- Evidência: célula rotulada em notebooks/analise.ipynb#total; ver https://exemplo.org/painel
"""
        root = self.project(spec=spec, plan=None, evidence=False)
        self.write(root, {'notebooks/analise.ipynb': '{}'})
        code, out = run(root)
        self.assertEqual(code, 0, out)

    def test_stage_a3_requires_evidence(self):
        root = self.project()
        self.assertEqual(run(root)[0], 0)
        code, out = run(root, '--stage', 'a3')
        self.assertEqual(code, 1)
        self.assertIn('R-002: requisito aprovado sem evidência antes do A3', out)

    def test_bold_fields_state_comment_fence_and_bom(self):
        spec = """### R-001 Filtro
- **Critério**: Dado o filtro, Então o total bate.
- **Estado**: aprovado (A1 de 2026-11-07)
```python
# comentário que não encerra o requisito
```
- Evidência: ver Python 3.9 e kiro.dev/docs; e.g. nada
### H-001 Hipótese
- Critério: a média sobe.
- Estado: proposto
"""
        root = self.write(self.tmp(), {'docs/plan.md': '### T-001 X\n- Requisitos: R-001\n'})
        (root / 'docs/spec.md').write_bytes(spec.encode('utf-8-sig'))
        code, out = run(root)
        self.assertEqual(code, 0, out)
        code, out = run(root, '--stage', 'a3')
        self.assertEqual(code, 1)
        self.assertIn('R-001: evidência cita arquivo que não existe: kiro.dev/docs', out)
        self.assertNotIn('3.9', out)

    def test_stage_a3_checks_evidence_exists_for_implemented(self):
        spec = SPEC.replace('- Estado: aprovado', '- Estado: implementado\n- Evidência: tests/test_exportar.py::test_r002')
        code, out = run(self.project(spec=spec), '--stage', 'a3')
        self.assertEqual(code, 1)
        self.assertIn('R-002: evidência cita arquivo que não existe: tests/test_exportar.py', out)

    def test_spec_without_requirements_is_a_problem(self):
        code, out = run(self.project(spec='# Spec\n## R-001 Nível errado\n', plan=None))
        self.assertEqual(code, 1)
        self.assertIn('nenhum requisito', out)

    def test_plan_traceability(self):
        code, out = run(self.project(plan='### T-001 Filtro\n- Requisitos: R-001, R-009\n### T-002 Solta\n'))
        self.assertEqual(code, 1)
        for msg in ('T-001: cita requisito que não existe: R-009', 'T-002: tarefa sem requisitos', 'R-002: requisito aprovado sem tarefa no plano'):
            self.assertIn(msg, out)

    def test_no_spec_bad_root_bad_argument_and_unreadable(self):
        self.assertEqual(run(self.tmp())[0], 2)
        self.assertEqual(run(Path('/nao/existe'))[0], 2)
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(sc.main(['--format', 'yaml']), 2)
            self.assertEqual(sc.main(['--help']), 2)
        root = self.tmp()
        (root / 'docs').mkdir()
        (root / 'docs/spec.md').write_bytes(b'\xff\xfe### R-001')
        self.assertEqual(run(root)[0], 2)


class External(Base):
    def test_eval_fixtures_are_clean(self):
        for name, fmt in (('sdd-speckit', 'speckit'), ('sdd-kiro', 'kiro'), ('sdd-openspec', 'openspec')):
            code, out = run(REPO / 'evals/fixtures' / name)
            self.assertEqual(code, 0, out)
            self.assertIn('formato: ' + fmt, out)

    def test_old_docs_have_no_spec(self):
        self.assertEqual(run(REPO / 'evals/fixtures/compat-docs-antigos')[0], 2)

    def test_speckit_unknown_story_and_requirement(self):
        d = self.write(self.tmp(), {
            '.specify/memory/constitution.md': '',
            'specs/001-x/spec.md': '### User Story 1 - X\n- **FR-001**: System MUST x.\n',
            'specs/001-x/tasks.md': '- [ ] T001 [US2] y\n- [ ] T002 FR-002\n',
        })
        code, out = run(d)
        self.assertEqual(code, 1)
        self.assertIn('cita US2', out)
        self.assertIn('cita FR-002', out)

    def test_empty_openspec_does_not_hide_native_spec(self):
        d = self.write(self.tmp(), {'docs/spec.md': SPEC, 'tests/test_filtro.py': ''})
        (d / 'openspec').mkdir()
        code, out = run(d)
        self.assertEqual(code, 0, out)
        self.assertIn('formato: native', out)

    def test_speckit_needs_specify_dir(self):
        d = self.write(self.tmp(), {'specs/001-x/spec.md': '', 'specs/001-x/plan.md': ''})
        self.assertEqual(run(d)[0], 2)

    def test_openspec_scenarios_removed_and_archive(self):
        o = self.write(self.tmp(), {
            'openspec/specs/a/spec.md': '## Requirements\n### Requirement: Sem cenário\nx\n## REMOVED Requirements\n### Requirement: Antigo\n',
            'openspec/specs/archive/spec.md': '### Requirement: Domínio chamado archive\n',
            'openspec/changes/archive/velha/spec.md': '### Requirement: Arquivada\n',
            'openspec/changes/c/tasks.md': '',
        })
        code, out = run(o)
        self.assertEqual(code, 1)
        self.assertIn('requisito sem cenário: Requirement: Sem cenário', out)
        self.assertIn('Domínio chamado archive', out)
        self.assertNotIn('Antigo', out)
        self.assertNotIn('Arquivada', out)
        self.assertIn('ainda em andamento: openspec/changes/c: falta proposal.md', out)
        code, out = run(o, '--stage', 'a3')
        self.assertIn('problema: openspec/changes/c: falta proposal.md', out)

    def test_kiro_incomplete_trio_only_fails_at_a3(self):
        k = self.write(self.tmp(), {'.kiro/specs/x/requirements.md': 'WHEN a THE SYSTEM SHALL b\n'})
        code, out = run(k)
        self.assertEqual(code, 0, out)
        self.assertIn('ainda em andamento', out)
        code, out = run(k, '--stage', 'a3')
        self.assertEqual(code, 1)
        self.assertIn('falta design.md', out)

    def test_explicit_format_and_second_format_warning(self):
        d = self.write(self.tmp(), {
            'docs/spec.md': SPEC.replace('verificado', 'aprovado'),
            '.kiro/specs/x/requirements.md': '', '.kiro/specs/x/design.md': '', '.kiro/specs/x/tasks.md': '',
        })
        code, out = run(d)
        self.assertEqual(code, 0, out)
        self.assertIn('formato: kiro', out)
        self.assertNotIn('aviso', out)
        code, out = run(d, '--stage', 'a3')
        self.assertEqual(code, 1)
        self.assertIn('problema: native: R-002: requisito aprovado sem evidência antes do A3', out)
        self.assertIn('evidência não conferida no formato kiro', out)
        code, out = run(d, '--format', 'native')
        self.assertEqual(code, 0, out)
        self.assertIn('formato: native', out)
        self.assertNotIn('aviso', out)


if __name__ == '__main__':
    unittest.main()
