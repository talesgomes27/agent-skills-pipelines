#!/usr/bin/env python3
"""PreToolUse do Bash: pede confirmação para os efeitos do catálogo. Nunca libera.

Procura cada efeito em qualquer ponto do comando, o que pega `git -C . push`,
`cd app && git push`, `env X=1 git push` e `bash -c "git push"`. Sem achado, não
decide e o fluxo normal de permissões segue. Entrada inválida sai com erro, e o
`onFailure: "block"` do hooks.json bloqueia em vez de deixar passar.
"""
import json
import re
import sys
from pathlib import Path

EFFECTS = Path(__file__).resolve().parents[1] / 'effects.json'


def decide(command, effects):
    for effect in effects:
        if re.search(effect['padrao'], command, re.S):
            return {'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'ask',
                'permissionDecisionReason': 'Efeito do catálogo das pipelines (%s): confirme alvo e conteúdo.' % effect['descricao'],
            }}
    return None


def main():
    sys.stderr.reconfigure(encoding='utf-8')  # o erro em stderr sai legível também no Windows
    effects = json.loads(EFFECTS.read_text(encoding='utf-8'))['efeitos']
    data = json.load(sys.stdin.buffer)  # bytes UTF-8, sem depender do encoding do console
    command = data.get('tool_input', {}).get('command', '')
    if not isinstance(command, str):
        raise ValueError('tool_input.command não é texto')
    out = decide(command, effects)
    if out:
        print(json.dumps(out))  # ASCII com escapes: lê igual em qualquer console, inclusive cp1252
    return 0


if __name__ == '__main__':
    sys.exit(main())
