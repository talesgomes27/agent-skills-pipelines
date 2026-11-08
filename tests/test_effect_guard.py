import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GUARD = REPO / 'pipeline-guardrails/scripts/effect_guard.py'
EFFECTS = json.loads((REPO / 'pipeline-guardrails/effects.json').read_text(encoding='utf-8'))['efeitos']

ASK = [
    'git push origin main',
    'git \\\n  push origin main',
    'git commit -m x &&\ngit push',
    'gh api repos/o/r/pulls/1/merge -X PUT',
    'docker push org/app:1.0',
    'quarto publish gh-pages',
    'Rscript -e "rsconnect::deployApp()"',
    'alembic -c x.ini upgrade head',
    'prisma db push',
    'poetry add httpx',
    'pip3.12 install rich',
    'gh api repos/o/r/merges -f base=main -f head=x',
    "gh api graphql -f query='mutation { mergePullRequest(input: {}) { clientMutationId } }'",
    'gh api repos/o/r/pulls -X POST -f title=x',
    'gh api repos/o/r/pulls -f title=x -f head=b -f base=main',
    'gh api --method=POST repos/o/r/pulls',
    'gh api repos/o/r/releases -f tag_name=v1',
    'gh api repos/o/r/git/refs -f ref=refs/tags/v1 -f sha=abc',
    'gh api repos/o/r/pulls --input body.json',
    'npm run deploy',
    'make deploy',
    'mkdocs gh-deploy',
    'alembic downgrade -1',
    'prisma migrate reset --force',
    'rake db:migrate',
    'flask db upgrade',
    'pipx install ruff',
    'uv tool install ruff',
    'brew install jq',
    'cargo install ripgrep',
    'gem install rails',
    'Rscript -e "pak::pak(\'dplyr\')"',
    'Rscript -e "BiocManager::install(\'x\')"',
    'npx netlify-cli deploy --prod',
    'gcloud run deploy app --source .',
    'wrangler deploy',
    'cargo publish',
    'gem push x.gem',
    'rails db:migrate',
    'knex migrate:latest',
    'dbmate up',
    'conda install numpy',
    'mamba install pandas',
    'Rscript -e "pak::pkg_install(\'dplyr\')"',
    'Rscript -e "remotes::install_github(\'a/b\')"',
    'Rscript -e "renv::install(\'x\')"',
    'git -C . push',
    'cd app && git push',
    'env X=1 git push',
    'bash -c "git push"',
    'git tag v1.0.0',
    'gh pr create --fill',
    'gh pr merge 12 --merge',
    'gh release create v1.0.0',
    'gh workflow run deploy.yml',
    'vercel deploy --prod',
    'npx vercel --prod',
    'rsconnect deploy shiny .',
    'npm publish',
    'uv publish',
    'alembic upgrade head',
    'python manage.py migrate',
    'pip install pandas',
    'uv pip install requests',
    'uv add httpx',
    'npm install express',
    'Rscript -e \'install.packages("dplyr")\'',
]
PASS = [
    'git status',
    'git diff main',
    'git log --oneline -5',
    'ls -la',
    'python -m pytest -q',
    'uv run pytest',
    'ruff check .',
    'npm test',
    'cat README.md',
    'gh api repos/o/r/pulls',
    'gh api repos/o/r/releases',
    'uv sync --locked',
    'npm ci',
    'gh pr view 12',
    'gcloud config list',
]


def run(payload):
    return subprocess.run([sys.executable, str(GUARD)], input=payload, capture_output=True, text=True, encoding='utf-8')


class EffectGuard(unittest.TestCase):
    def test_effects_ask(self):
        for command in ASK:
            with self.subTest(command=command):
                r = run(json.dumps({'tool_input': {'command': command}}))
                self.assertEqual(r.returncode, 0, r.stderr)
                out = json.loads(r.stdout)['hookSpecificOutput']
                self.assertEqual((out['hookEventName'], out['permissionDecision']), ('PreToolUse', 'ask'))
                self.assertTrue(out['permissionDecisionReason'])

    def test_read_only_commands_do_not_decide(self):
        for command in PASS:
            with self.subTest(command=command):
                r = run(json.dumps({'tool_input': {'command': command}}))
                self.assertEqual((r.returncode, r.stdout), (0, ''), r.stderr)

    def test_never_allows(self):
        for command in ASK + PASS:
            r = run(json.dumps({'tool_input': {'command': command}}))
            self.assertNotIn('"allow"', r.stdout)

    def test_invalid_input_fails_so_the_hook_blocks(self):
        self.assertNotEqual(run('não é json').returncode, 0)
        self.assertNotEqual(run(json.dumps({'tool_input': {'command': ['git', 'push']}})).returncode, 0)
        hooks = json.loads((REPO / 'pipeline-guardrails/hooks/hooks.json').read_text(encoding='utf-8'))
        hook = hooks['hooks']['PreToolUse'][0]['hooks'][0]
        self.assertEqual((hook['onFailure'], hook['type']), ('block', 'command'))
        self.assertEqual(hooks['hooks']['PreToolUse'][0]['matcher'], 'Bash|PowerShell')

    def test_effects_exist_in_contract_catalog(self):
        contract = (REPO / 'shared/common-contract.md').read_text(encoding='utf-8')
        for e in EFFECTS:
            self.assertIn('| ' + e['catalogo'], contract)


if __name__ == '__main__':
    unittest.main()
