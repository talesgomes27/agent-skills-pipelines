"""Harness do nível de execução do /cenarios, só com a biblioteca padrão.

  plugin <saida>                       monta o plugin de teste "asp" com todas as skills e os subagentes
  preparar <exec> <pedido> [fixture]   cria <exec>/proj (cópia da fixture ou vazia) e <exec>/pedido.txt
  rodar <exec> <destino> [--plugin P] [--turnos N] [--aceite TEXTO]
                                       destino claude-code (plugin de teste) ou claude-code-instalador (skills.py)
  resumo <log>                         ferramentas, skills, negações e texto final de um log stream-json
  gatilho <log> <skill>                ativou, nao_ativou ou outra
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
ALLOW = ['Read', 'Glob', 'Grep', 'Bash(ls:*)', 'Bash(cat:*)', 'Bash(head:*)', 'Bash(wc:*)', 'Bash(grep:*)',
         'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(python3 -m pytest:*)', 'Bash(pytest:*)']


def plugin(saida):
    asp = Path(saida) / 'asp'
    shutil.rmtree(asp, ignore_errors=True)
    for s in sorted(p.parent for p in REPO.glob('*/SKILL.md')):
        shutil.copytree(s, asp / 'skills' / s.name, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(REPO / 'plugin-agents', asp / 'agents')
    # o hook do pipeline-guardrails, como no marketplace real; effect_guard.py acha o effects.json em parents[1]
    g = REPO / 'pipeline-guardrails'
    shutil.copytree(g / 'hooks', asp / 'hooks')
    shutil.copytree(g / 'scripts', asp / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy(g / 'effects.json', asp)
    versao = json.loads((REPO / 'distribution/catalog.json').read_text(encoding='utf-8'))['release']
    (asp / '.claude-plugin').mkdir()
    (asp / '.claude-plugin/plugin.json').write_text(json.dumps({'name': 'asp', 'version': versao, 'description': 'cópia de teste'}))
    print(asp)


def preparar(exe, pedido, fixture=None):
    exe = Path(exe)
    if fixture:
        shutil.copytree(REPO / 'evals' / fixture, exe / 'proj')
    else:
        (exe / 'proj').mkdir(parents=True)
    (exe / 'pedido.txt').write_text(pedido, encoding='utf-8')


def ler(log):
    for linha in open(log, encoding='utf-8'):
        try:
            yield json.loads(linha)
        except ValueError:
            continue


def _claude(proj, texto, log, plugin_dir, turnos, sessao=None):
    cmd = ['claude', '-p', texto, '--model', 'sonnet', '--max-turns', str(turnos), '--max-budget-usd', '1.5',
           '--output-format', 'stream-json', '--verbose', '--setting-sources', 'project', '--strict-mcp-config',
           '--permission-mode', 'acceptEdits', '--allowedTools', *ALLOW]
    if plugin_dir:
        cmd += ['--plugin-dir', str(plugin_dir)]
    if sessao:
        cmd += ['--resume', sessao]
    with open(log, 'w', encoding='utf-8') as out:
        try:
            return subprocess.run(cmd, cwd=proj, stdout=out, stderr=subprocess.DEVNULL, timeout=1500).returncode
        except subprocess.TimeoutExpired:
            return 124


def rodar(exe, destino, plugin_dir=None, turnos=40, aceite=None):
    exe = Path(exe)
    if (exe / 'done').exists():
        return
    for velho in ('log2.jsonl', 'aceite_pulado', 'erro_api'):
        (exe / velho).unlink(missing_ok=True)
    proj = exe / 'proj'
    if destino == 'claude-code-instalador':
        # escopo project: não toca o ~/.claude/skills/ do usuário; sem subagentes nem hook do pipeline-guardrails
        subprocess.run([sys.executable, str(REPO / 'scripts/skills.py'), 'install', '--agent', 'claude', '--scope', 'project',
                        '--project', str(proj), '--all', '--mode', 'copy'], check=True, stdout=subprocess.DEVNULL)
        plugin_dir = None
    elif not plugin_dir:
        sys.exit('o destino claude-code pede --plugin')
    codigo = _claude(proj, (exe / 'pedido.txt').read_text(encoding='utf-8'), exe / 'log.jsonl', plugin_dir, turnos)
    fim = [d for d in ler(exe / 'log.jsonl') if d.get('type') == 'result']
    if aceite and fim and fim[-1].get('subtype') == 'success':
        # segundo turno: o aceite do usuário simulado, na mesma sessão; não roda se o primeiro estourou turnos ou orçamento
        codigo = _claude(proj, aceite, exe / 'log2.jsonl', plugin_dir, turnos, fim[-1]['session_id'])
    elif aceite:
        (exe / 'aceite_pulado').write_text('o primeiro turno não terminou com success')
    erros = [d for log in ('log.jsonl', 'log2.jsonl') if (exe / log).exists() for d in ler(exe / log)
             if d.get('type') == 'result' and d.get('api_error')]
    if erros:
        # limite de uso ou falha da API não é resultado da skill: sem done, a execução roda de novo
        (exe / 'erro_api').write_text(str(erros[-1]['api_error']))
        return
    (exe / 'done').write_text(str(codigo))


def skills(log):
    return [c['input'].get('skill', '') for d in ler(log) if d.get('type') == 'assistant'
            for c in d['message'].get('content', []) if c.get('type') == 'tool_use' and c['name'] == 'Skill']


def gatilho(log, skill):
    # o plugin de teste prefixa asp:, e o marketplace real usa <plugin>:<skill>
    nomes = [s.split(':')[-1] for s in skills(log)]
    return 'ativou' if skill in nomes else ('outra' if nomes else 'nao_ativou')


def resumo(log):
    tools, texts, res, init = [], [], {}, {}
    for d in ler(log):
        if d.get('type') == 'system' and d.get('subtype') == 'init':
            init = d
        elif d.get('type') == 'assistant':
            for c in d['message'].get('content', []):
                if c.get('type') == 'tool_use':
                    tools.append(c['name'] + ': ' + json.dumps(c['input'], ensure_ascii=False)[:160])
                elif c.get('type') == 'text':
                    texts.append(c['text'])
        elif d.get('type') == 'result':
            res = d
    # isolamento: só as skills do repositório (com ou sem asp:) e as do próprio Claude Code
    print('INIT', init.get('model'), 'skills:', init.get('skills'))
    print('TOOLS', len(tools), *tools, sep='\n  ')
    print('SKILLS', skills(log))
    print('DENIALS', json.dumps(res.get('permission_denials', []), ensure_ascii=False)[:1500])
    print('RESULT', res.get('subtype'), 'turns', res.get('num_turns'), 'cost', res.get('total_cost_usd'))
    print('FINAL TEXT:\n', (texts[-1] if texts else '')[:3000])


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('plugin').add_argument('saida')
    p = sub.add_parser('preparar')
    p.add_argument('exe'); p.add_argument('pedido'); p.add_argument('fixture', nargs='?')
    p = sub.add_parser('rodar')
    p.add_argument('exe'); p.add_argument('destino', choices=['claude-code', 'claude-code-instalador'])
    p.add_argument('--plugin'); p.add_argument('--turnos', type=int, default=40); p.add_argument('--aceite')
    sub.add_parser('resumo').add_argument('log')
    p = sub.add_parser('gatilho')
    p.add_argument('log'); p.add_argument('skill')
    x = ap.parse_args()
    if x.cmd == 'plugin':
        plugin(x.saida)
    elif x.cmd == 'preparar':
        preparar(x.exe, x.pedido, x.fixture)
    elif x.cmd == 'rodar':
        rodar(x.exe, x.destino, x.plugin, x.turnos, x.aceite)
    elif x.cmd == 'resumo':
        resumo(x.log)
    else:
        print(gatilho(x.log, x.skill))
