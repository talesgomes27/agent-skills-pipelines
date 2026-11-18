"""Harness do nível de execução do /cenarios, só com a biblioteca padrão.

  plugin <saida>                       monta em <saida>/plugins um plugin por entrada do marketplace
  preparar <exec> <pedido> [fixture]   cria <exec>/proj (cópia da fixture ou vazia) e <exec>/pedido.txt
  rodar <exec> <destino> [--plugin P] [--turnos N] [--aceite TEXTO]
                                       destino claude-code (plugin de teste), claude-code-instalador (skills.py)
                                       ou sem-skill (nenhuma skill do repositório: o braço de comparação dos cenários)
  resumo <log>                         ferramentas, skills, negações e texto final de um log stream-json
  gatilho <log> <skill>                ativou, nao_ativou ou outra
  lote <pasta> [--cenarios a,b] [--gatilhos a,b|todos] [--destinos d1,d2] [--amostras N] [--paralelo N]
                                       --destinos aceita sem-skill, que roda só os cenários; prepara e roda as execuções em <pasta>/<destino>/exec-<hash>-<n>, com o id no meta.json, retomando as
                                       que ficaram sem done; o plugin de teste vai para <pasta>/plugin
  contar <pasta> [--contra VERSAO] [--json]
                                       gatilhos ativou/total por destino e skills carregadas nos cenários,
                                       comparados com evals/results/VERSAO quando pedido; ambiguo_deve conta como deve;
                                       com --json, os resultados com amostras e as metricas de cada triggers-<destino>.json
  metricas <exec>                      custo_usd, turnos, duracao_ms e tokens da execução, em JSON; ausente é null
  estado <exec> [--fixture F]          arquivos criados, apagados e alterados contra a fixture, comandos Bash com o
                                       erro e a última linha da saída, skills e tentativas de efeito no git, em JSON
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
ALLOW = ['Read', 'Glob', 'Grep', 'Bash(ls:*)', 'Bash(cat:*)', 'Bash(head:*)', 'Bash(wc:*)', 'Bash(grep:*)',
         'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(python3 -m pytest:*)', 'Bash(python -m pytest:*)', 'Bash(pytest:*)']


def plugin(saida):
    # um plugin por entrada do marketplace.json, com o mesmo nome e prefixo <plugin>:<skill> da instalação real;
    # --plugin-dir carrega cada filho de uma pasta de plugins
    raiz = Path(saida).resolve() / 'plugins'  # absoluto: o claude roda dentro de <exec>/proj
    shutil.rmtree(raiz, ignore_errors=True)
    versao = json.loads((REPO / 'distribution/catalog.json').read_text(encoding='utf-8'))['release']
    sem = shutil.ignore_patterns('__pycache__')
    for p in json.loads((REPO / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))['plugins']:
        if p.get('dependencies'):
            continue  # pacote: só traz outros plugins
        d = raiz / p['name']
        if p['source'] != './':
            shutil.copytree(REPO / p['source'], d, ignore=sem)  # pipeline-guardrails, com o hook
            continue
        for s in p.get('skills', []):
            shutil.copytree(REPO / s, d / 'skills' / Path(s).name, ignore=sem)
        for a in p.get('agents', []):
            (d / 'agents').mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO / a, d / 'agents')
        (d / '.claude-plugin').mkdir(parents=True)
        (d / '.claude-plugin/plugin.json').write_text(json.dumps({'name': p['name'], 'version': versao, 'description': 'cópia de teste'}))
    print(raiz)


def preparar(exe, pedido, fixture=None):
    exe = Path(exe)
    if fixture:
        shutil.copytree(REPO / 'evals' / fixture, exe / 'proj')
    else:
        (exe / 'proj').mkdir(parents=True)
    (exe / 'pedido.txt').write_text(pedido, encoding='utf-8')


def ler(log):
    with open(log, encoding='utf-8') as f:  # fechado já ao fim: no Windows, arquivo aberto impede apagar a pasta
        for linha in f:
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
    elif destino == SEM_SKILL:
        plugin_dir = None  # nem plugin nem instalação: o que passa aqui não depende da skill
    elif not plugin_dir:
        sys.exit('o destino claude-code pede --plugin')
    else:
        plugin_dir = Path(plugin_dir).resolve()  # relativo, o claude o procuraria dentro de proj
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
    # plugin: <plugin>:<skill>; instalador: sem prefixo
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
    # isolamento: só as skills do repositório (com ou sem o prefixo do plugin) e as do próprio Claude Code
    print('INIT', init.get('model'), 'skills:', init.get('skills'))
    print('TOOLS', len(tools), *tools, sep='\n  ')
    print('SKILLS', skills(log))
    print('DENIALS', json.dumps(res.get('permission_denials', []), ensure_ascii=False)[:1500])
    print('RESULT', res.get('subtype'), 'turns', res.get('num_turns'), 'cost', res.get('total_cost_usd'))
    print('FINAL TEXT:\n', (texts[-1] if texts else '')[:3000])


IGNORAR = {'.claude', '.git', '.venv', '__pycache__', '.pytest_cache'}  # .claude: no instalador, quem grava é o harness
# tentativas de efeito no git e no gh, com opções globais antes do subcomando; a negação fica no erro do comando
GIT_EFEITO = re.compile(r'\bgit\b(?:\s+-[Cc]\s+\S+|\s+--?\S+)*\s+(?:push|commit|reset|checkout|clean|rebase|restore|stash|branch\s+-D)(?![\w-])'
                        r'|\bgh\s+pr\s+(?:create|merge)\b')


def _texto(conteudo):
    if isinstance(conteudo, list):
        return '\n'.join(c.get('text', '') for c in conteudo if isinstance(c, dict))
    return conteudo or ''


def _fixture_do_meta(exe):
    """Fixture da execução: do meta.json; num meta.json antigo, sem a chave, do cenário."""
    meta = json.loads((exe / 'meta.json').read_text()) if (exe / 'meta.json').exists() else {}
    if 'fixture' in meta:
        return meta['fixture']
    if meta.get('tipo') == 'cenario' and (REPO / f"evals/scenarios/{meta.get('id')}.yaml").exists():
        return _yaml(REPO / f"evals/scenarios/{meta['id']}.yaml").get('fixture')
    if meta.get('tipo') == 'gatilho' and meta.get('id') in (T := _gatilhos()):
        return T[meta['id']].get('fixture')
    sys.exit('sem meta.json com a fixture: passe --fixture, ou --fixture "" para um proj que começou vazio')


def estado(exe, fixture=None):
    """Fatos determinísticos de uma execução, para o juiz ler antes do log: arquivos, comandos e skills."""
    exe = Path(exe)
    fixture = _fixture_do_meta(exe) if fixture is None else (fixture or None)
    if fixture and not (REPO / 'evals' / fixture).is_dir():
        sys.exit(f'fixture inexistente: evals/{fixture}')

    def arquivos(raiz):
        out = {}
        for f in raiz.rglob('*') if raiz else ():
            rel = f.relative_to(raiz)
            if IGNORAR & set(rel.parts) or not (f.is_file() or f.is_symlink()):
                continue
            try:
                out[str(rel)] = f.read_bytes()
            except OSError as e:  # link quebrado ou sem permissão: ainda conta como existente
                out[str(rel)] = repr(e).encode()
        return out
    antes, depois = arquivos(REPO / 'evals' / fixture if fixture else None), arquivos(exe / 'proj')
    usos, resultados = {}, {}
    for log in ('log.jsonl', 'log2.jsonl'):
        if not (exe / log).exists():
            continue
        for d in ler(exe / log):
            for c in (d.get('message') or {}).get('content', []) if d.get('type') in ('assistant', 'user') else []:
                if not isinstance(c, dict):
                    continue
                if c.get('type') == 'tool_use' and c['name'] == 'Bash':
                    usos[c['id']] = (log, c['input'].get('command', ''), bool(d.get('parent_tool_use_id')))
                elif c.get('type') == 'tool_result' and c.get('tool_use_id') in usos:
                    linhas = _texto(c.get('content')).strip().splitlines()
                    resultados[c['tool_use_id']] = (bool(c.get('is_error')), linhas[-1][:200] if linhas else '')
    comandos, git = [], []
    for i, (log, cmd, sub) in usos.items():
        erro, ultima = resultados.get(i, (None, ''))  # None: sem resultado no log (limite de turnos, timeout)
        c = {'turno': 2 if log == 'log2.jsonl' else 1, 'comando': cmd[:300], 'erro': erro, 'ultima_linha': ultima}
        if sub:
            c['subagente'] = True
        comandos.append(c)
        if GIT_EFEITO.search(cmd):  # no comando inteiro: um heredoc longo não esconde o git do fim
            git.append(c)
    return {'fixture': fixture,
            'criados': sorted(set(depois) - set(antes)),
            'apagados': sorted(set(antes) - set(depois)),
            'alterados': sorted(f for f in set(antes) & set(depois) if antes[f] != depois[f]),
            'skills': [s.split(':')[-1] for log in ('log.jsonl', 'log2.jsonl') if (exe / log).exists() for s in skills(exe / log)],
            'comandos': comandos, 'git_efeito': git}


TOKENS = {'entrada': 'input_tokens', 'saida': 'output_tokens', 'cache_leitura': 'cache_read_input_tokens',
          'cache_escrita': 'cache_creation_input_tokens'}


def metricas(exe):
    """Custo, turnos, duração e tokens do evento result de log.jsonl e log2.jsonl, somados.

    Um valor que nenhum log traz fica None, nunca 0: desconhecido não é de graça."""
    fins = []
    for nome in ('log.jsonl', 'log2.jsonl'):
        if (Path(exe) / nome).exists():
            fins += [d for d in ler(Path(exe) / nome) if d.get('type') == 'result'][-1:]

    def soma(valores):
        valores = [v for v in valores if isinstance(v, (int, float))]
        return round(sum(valores), 6) if valores else None
    usos = [f['usage'] for f in fins if isinstance(f.get('usage'), dict)]
    return {'custo_usd': soma(f.get('total_cost_usd') for f in fins), 'turnos': soma(f.get('num_turns') for f in fins),
            'duracao_ms': soma(f.get('duration_ms') for f in fins),
            'tokens': {k: soma(u.get(v) for u in usos) for k, v in TOKENS.items()} if usos else None}


DESTINOS = ('claude-code', 'claude-code-instalador')
SEM_SKILL = 'sem-skill'  # fora do padrão do lote: dobra o custo e só serve aos cenários


def _yaml(caminho):
    import yaml  # o PyYAML já é dependência do repositório (distribution/requirements.txt)
    return yaml.safe_load(Path(caminho).read_text(encoding='utf-8'))


def _gatilhos():
    return {t['id']: t for t in _yaml(REPO / 'evals/triggers.yaml')}


def lote(pasta, cenarios=(), gatilhos=(), destinos=DESTINOS, amostras=1, paralelo=4):
    from concurrent.futures import ThreadPoolExecutor
    pasta = Path(pasta)
    if set(destinos) - {*DESTINOS, SEM_SKILL}:
        sys.exit(f'destino desconhecido; use {", ".join(DESTINOS)} ou {SEM_SKILL}')
    pasta.mkdir(parents=True, exist_ok=True)
    trava = pasta / '.lote-em-andamento'
    if trava.exists():
        try:
            os.kill(int(trava.read_text()), 0)
            sys.exit(f'outro lote ainda roda nesta pasta (pid {trava.read_text()}); espere ele terminar')
        except (ValueError, ProcessLookupError):
            pass  # trava de um lote que morreu
    trava.write_text(str(os.getpid()))
    if not (pasta / 'plugin/plugins').exists():
        plugin(pasta / 'plugin')
    T = _gatilhos()
    if list(gatilhos) == ['todos']:
        gatilhos = list(T)
    itens = [('cenario', i, _yaml(REPO / f'evals/scenarios/{i}.yaml')) for i in cenarios]
    itens += [('gatilho', i, T[i]) for i in gatilhos]
    jobs = []
    for destino in destinos:
        for tipo, i, d in itens:
            if destino == SEM_SKILL and tipo == 'gatilho':
                continue  # sem a skill, um gatilho nunca ativa
            for n in range(1, amostras + 1):
                # nome neutro: o claude vê o caminho, e um id com o nome da skill o levava a carregá-la; o id fica no meta.json
                exe = pasta / destino / f"exec-{hashlib.sha1(f'{tipo}-{i}'.encode()).hexdigest()[:8]}-{n}"
                if (exe / 'done').exists():
                    continue
                if exe.exists():
                    shutil.rmtree(exe)  # sem done: erro de API ou execução interrompida; a cópia pode ter sido editada
                preparar(exe, d['pedido'] if tipo == 'cenario' else d['prompt'], d.get('fixture'))
                (exe / 'meta.json').write_text(json.dumps({'tipo': tipo, 'id': i, 'destino': destino, 'amostra': n,
                                                           'fixture': d.get('fixture')}))
                aceite = d.get('aceite_simulado') if tipo == 'cenario' else None
                jobs.append((exe, destino, 40 if tipo == 'cenario' else 8, aceite))
    print(len(jobs), 'execuções')

    def um(j):
        try:
            rodar(j[0], j[1], pasta / 'plugin/plugins', j[2], j[3])
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


def contar(pasta, contra=None, json_saida=False):
    import collections
    pasta = Path(pasta)
    T = _gatilhos()
    gat = collections.defaultdict(list)
    met = collections.defaultdict(list)
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
            met[m['destino']].append(metricas(exe))
        else:
            sk = [s.split(':')[-1] for s in skills(exe / 'log.jsonl')] or ['(nenhuma)']
            for s in set(sk):
                cen[(m['destino'], m['id'])][s] += 1
            cen[(m['destino'], m['id'])]['_total'] += 1
    if json_saida:
        # resultados e metricas do triggers-<destino>.json; uma amostra errada faz do erro o observado
        out = {}
        for destino in DESTINOS:
            res = []
            for (d, i), obs in sorted(gat.items()):
                if d != destino:
                    continue
                esperado = T[i]['esperado']
                certo = ((lambda o: True) if esperado == 'opcional' else
                         (lambda o: o != 'ativou') if esperado == 'nao_deve' else (lambda o: o == 'ativou'))
                res.append({'id': i, 'observado': next((o for o in obs if not certo(o)), obs[0]), 'amostras': obs})
            if res:
                ms = met[destino]
                soma = lambda k: round(sum(x[k] for x in ms if x[k] is not None), 6)
                out[destino] = {'resultados': res, 'metricas': {'custo_usd': soma('custo_usd'), 'turnos': soma('turnos'),
                                'duracao_ms': soma('duracao_ms'), 'sem_custo': sum(x['custo_usd'] is None for x in ms)}}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    for destino in DESTINOS:
        linhas = sorted((i, obs) for (d, i), obs in gat.items() if d == destino)
        if not linhas:
            continue
        antes = {}
        if contra:
            f = REPO / f'evals/results/{contra}/execucao/triggers-{destino}.json'
            if f.exists():
                antes = {r['id']: r['observado'] for r in json.loads(f.read_text(encoding='utf-8'))['resultados']}
        certos = contados = 0
        print(f'\n## Gatilhos, {destino}')
        for i, obs in linhas:
            esperado = T[i]['esperado']
            extra = f' | {contra}: {antes[i]}' if i in antes else ''
            if esperado == 'opcional':  # ativar ou não são ambos aceitáveis: fora da conta
                print(f'{i:40} {esperado:12} fora da conta ({" ".join(o[:3] for o in obs)}){extra}')
                continue
            ok = sum((o != 'ativou') if esperado == 'nao_deve' else (o == 'ativou') for o in obs)
            certos += ok == len(obs)
            contados += 1
            print(f'{i:40} {esperado:12} {ok}/{len(obs)} certos ({" ".join(o[:3] for o in obs)}){extra}')
        print(f'{certos} de {contados} gatilhos certos em todas as amostras')
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
    p.add_argument('exe'); p.add_argument('destino', choices=[*DESTINOS, SEM_SKILL])
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
    p.add_argument('pasta'); p.add_argument('--contra'); p.add_argument('--json', action='store_true')
    sub.add_parser('metricas').add_argument('exe')
    p = sub.add_parser('estado')
    p.add_argument('exe'); p.add_argument('--fixture')
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
        contar(x.pasta, x.contra, x.json)
    elif x.cmd == 'metricas':
        print(json.dumps(metricas(x.exe)))
    elif x.cmd == 'estado':
        print(json.dumps(estado(x.exe, x.fixture), ensure_ascii=False, indent=1))
    else:
        print(gatilho(x.log, x.skill))
