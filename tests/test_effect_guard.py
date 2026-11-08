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
    'gh api repos/o/r/contents/x.md -X PUT -f message=x -f content=eA==',
    'gh api repos/o/r/contents/x.md --method DELETE -f sha=abc',
    'gh api repos/o/r/dispatches -f event_type=deploy',
    'gh api repos/o/r/actions/workflows/ci.yml/dispatches -f ref=main',
    "gh api graphql -f query='mutation { createRef(input: {}) { clientMutationId } }'",
    "gh api graphql -f query='mutation { createCommitOnBranch(input: {}) { clientMutationId } }'",
    'curl -X POST https://api.github.com/repos/o/r/git/refs -d @ref.json',
    'curl --request PUT -H "Authorization: token $T" https://api.github.com/repos/o/r/contents/x',
    'curl -d \'{"ref":"main"}\' https://api.github.com/repos/o/r/dispatches',
    'vercel',
    'vercel --prod',
    './node_modules/.bin/vercel --prod',
    'gh api repos/o/r/contents/a.md --method="PUT" -f message=x',
    "gh api --method 'PUT' repos/o/r/contents/a.md",
    'gh api -X put repos/o/r/contents/a.md',
    'gh api -X PATCH repos/o/r/git/refs/heads/main -f sha=abc',
    "gh api graphql -f query='mutation { updateRef(input: {}) { clientMutationId } }'",
    "gh api graphql -f query='mutation { deleteRef(input: {}) { clientMutationId } }'",
    'gh api graphql -F query=@mutation.graphql',
    'gh api graphql --input q.json',
    'curl -sXPUT https://api.github.com/repos/o/r/contents/a.md',
    "curl -d'{}' https://api.github.com/repos/o/r/dispatches",
    'curl -d@ref.json https://api.github.com/repos/o/r/git/refs',
    "curl --json '{}' https://api.github.com/repos/o/r/dispatches",
    'curl -T a.md https://api.github.com/repos/o/r/contents/a.md',
    'curl --upload-file a.md https://api.github.com/repos/o/r/contents/a.md',
    'curl -X post https://api.github.com/repos/o/r/pulls',
    'curl --request=PATCH https://api.github.com/repos/o/r/pulls/1',
    'curl --data-binary @x https://uploads.github.com/repos/o/r/releases/1/assets',
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
    'cat vercel.json',
    'cat .vercel/project.json',
    'grep -n vercel- README.md',
    'gh api repos/o/r/contents/README.md',
    'gh api repos/o/r/actions/workflows',
    'curl -s https://api.github.com/repos/o/r',
    'gh api repos/o/r/pulls -f state=open -X GET',
    'gh api -X GET repos/o/r/contents/a -f ref=main',
    'curl -sSL -H "Accept: application/json" https://api.github.com/repos/o/r/contents/a',
    'cat app/vercel.json',
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
