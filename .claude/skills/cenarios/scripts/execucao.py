"""Harness do nível de execução do /cenarios, só com a biblioteca padrão.

  plugin <saida>                       monta o plugin de teste "asp" com todas as skills e os subagentes
  preparar <exec> <pedido> [fixture]   cria <exec>/proj (cópia da fixture ou vazia) e <exec>/pedido.txt
  rodar <exec> <destino> [--plugin P] [--turnos N] [--aceite TEXTO]
                                       destino claude-code (plugin de teste) ou claude-code-instalador (skills.py)
  resumo <log>                         ferramentas, skills, negações e texto final de um log stream-json
  gatilho <log> <skill>                ativou, nao_ativou ou outra
  lote <pasta> [--cenarios a,b] [--gatilhos a,b|todos] [--destinos d1,d2] [--amostras N] [--paralelo N]
                                       prepara e roda as execuções em <pasta>/<destino>/<tipo>-<id>-<n>, retomando as
                                       que ficaram sem done; o plugin de teste vai para <pasta>/plugin
  contar <pasta> [--contra VERSAO]     gatilhos ativou/total por destino e skills carregadas nos cenários,
                                       comparados com evals/results/VERSAO quando pedido; ambiguo_deve conta como deve
"""
import json
import os
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


DESTINOS = ('claude-code', 'claude-code-instalador')


def _yaml(caminho):
    import yaml  # o PyYAML já é dependência do repositório (distribution/requirements.txt)
    return yaml.safe_load(Path(caminho).read_text(encoding='utf-8'))


def _gatilhos():
    return {t['id']: t for t in _yaml(REPO / 'evals/triggers.yaml')}


def lote(pasta, cenarios=(), gatilhos=(), destinos=DESTINOS, amostras=1, paralelo=4):
    from concurrent.futures import ThreadPoolExecutor
    pasta = Path(pasta)
    if set(destinos) - set(DESTINOS):
        sys.exit(f'destino desconhecido; use {", ".join(DESTINOS)}')
    pasta.mkdir(parents=True, exist_ok=True)
    trava = pasta / '.lote-em-andamento'
    if trava.exists():
        try:
            os.kill(int(trava.read_text()), 0)
            sys.exit(f'outro lote ainda roda nesta pasta (pid {trava.read_text()}); espere ele terminar')
        except (ValueError, ProcessLookupError):
            pass  # trava de um lote que morreu
    trava.write_text(str(os.getpid()))
    if not (pasta / 'plugin/asp').exists():
        plugin(pasta / 'plugin')
    T = _gatilhos()
    if list(gatilhos) == ['todos']:
        gatilhos = list(T)
    itens = [('cenario', i, _yaml(REPO / f'evals/scenarios/{i}.yaml')) for i in cenarios]
    itens += [('gatilho', i, T[i]) for i in gatilhos]
    jobs = []
    for destino in destinos:
        for tipo, i, d in itens:
            for n in range(1, amostras + 1):
                exe = pasta / destino / f'{tipo}-{i}-{n}'
                if (exe / 'done').exists():
                    continue
                if exe.exists():
                    shutil.rmtree(exe)  # sem done: erro de API ou execução interrompida; a cópia pode ter sido editada
                preparar(exe, d['pedido'] if tipo == 'cenario' else d['prompt'], d.get('fixture'))
                (exe / 'meta.json').write_text(json.dumps({'tipo': tipo, 'id': i, 'destino': destino, 'amostra': n}))
                aceite = d.get('aceite_simulado') if tipo == 'cenario' else None
                jobs.append((exe, destino, 40 if tipo == 'cenario' else 8, aceite))
    print(len(jobs), 'execuções')

    def um(j):
        try:
            rodar(j[0], j[1], pasta / 'plugin/asp', j[2], j[3])
        except BaseException as e:  # inclui o sys.exit e o CalledProcessError do install: fica gravado, a rodada segue
            (j[0] / 'erro_local').write_text(repr(e))
    try:
        with ThreadPoolExecutor(paralelo) as ex:
            list(ex.map(um, jobs))
    finally:
        trava.unlink(missing_ok=True)
    api = sum((j[0] / 'erro_api').exists() for j in jobs)
    local = sum((j[0] / 'erro_local').exists() for j in jobs)
    print(len(jobs) - api - local, 'concluídas;', api, 'com erro da API e', local, 'com erro local (rode lote de novo para retomá-las)')


def contar(pasta, contra=None):
    import collections
    pasta = Path(pasta)
    T = _gatilhos()
    gat = collections.defaultdict(list)
    cen = collections.defaultdict(collections.Counter)
    pendentes = 0
    invalidas = 0
    for meta in sorted(pasta.glob('*/*/meta.json')):
        try:
            m = json.loads(meta.read_text())
            if m['tipo'] == 'gatilho' and m['id'] not in T:
                raise KeyError(m['id'])
        except (ValueError, KeyError):
            invalidas += 1
            continue
        exe = meta.parent
        if not (exe / 'done').exists():
            pendentes += 1
            continue
        if m['tipo'] == 'gatilho':
            gat[(m['destino'], m['id'])].append(gatilho(exe / 'log.jsonl', T[m['id']]['skill']))
        else:
            sk = [s.split(':')[-1] for s in skills(exe / 'log.jsonl')] or ['(nenhuma)']
            for s in set(sk):
                cen[(m['destino'], m['id'])][s] += 1
            cen[(m['destino'], m['id'])]['_total'] += 1
    for destino in DESTINOS:
        linhas = sorted((i, obs) for (d, i), obs in gat.items() if d == destino)
        if not linhas:
            continue
        antes = {}
        if contra:
            f = REPO / f'evals/results/{contra}/execucao/triggers-{destino}.json'
            if f.exists():
                antes = {r['id']: r['observado'] for r in json.loads(f.read_text(encoding='utf-8'))['resultados']}
        certos = 0
        print(f'\n## Gatilhos, {destino}')
        for i, obs in linhas:
            esperado = T[i]['esperado']
            ok = sum((o != 'ativou') if esperado == 'nao_deve' else (o == 'ativou') for o in obs)
            certos += ok == len(obs)
            extra = f' | {contra}: {antes[i]}' if i in antes else ''
            print(f'{i:40} {esperado:12} {ok}/{len(obs)} certos ({" ".join(o[:3] for o in obs)}){extra}')
        print(f'{certos} de {len(linhas)} gatilhos certos em todas as amostras')
    for (destino, i), c in sorted(cen.items()):
        total = c.pop('_total')
        print(f'cenário {i} ({destino}): {total} execuções; skills: ' + ', '.join(f'{s} {n}' for s, n in c.most_common()))
    if pendentes:
        print(f'\n{pendentes} execuções sem done (erro da API, erro local ou em andamento)')
    if invalidas:
        print(f'{invalidas} pastas com meta.json inválido ou gatilho que saiu do triggers.yaml, ignoradas')


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
    p = sub.add_parser('lote')
    lista = lambda v: [x for x in v.split(',') if x]
    p.add_argument('pasta'); p.add_argument('--cenarios', type=lista, default=[]); p.add_argument('--gatilhos', type=lista, default=[])
    p.add_argument('--destinos', type=lista, default=list(DESTINOS)); p.add_argument('--amostras', type=int, default=1)
    p.add_argument('--paralelo', type=int, default=4)
    p = sub.add_parser('contar')
    p.add_argument('pasta'); p.add_argument('--contra')
    x = ap.parse_args()
    if x.cmd == 'plugin':
        plugin(x.saida)
    elif x.cmd == 'preparar':
        preparar(x.exe, x.pedido, x.fixture)
    elif x.cmd == 'rodar':
        rodar(x.exe, x.destino, x.plugin, x.turnos, x.aceite)
    elif x.cmd == 'resumo':
        resumo(x.log)
    elif x.cmd == 'lote':
        lote(x.pasta, x.cenarios, x.gatilhos, x.destinos, x.amostras, x.paralelo)
    elif x.cmd == 'contar':
        contar(x.pasta, x.contra)
    else:
        print(gatilho(x.log, x.skill))
