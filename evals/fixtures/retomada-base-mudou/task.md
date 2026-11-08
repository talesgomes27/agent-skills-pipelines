```yaml
pipeline: execution-pipeline
gate: EX-5
estado: aguardando_aprovacao
execucao: null
modo: por-efeito
esforco: padrao
aprovacoes:
  - item: plano de arredondamento de preços (docs/05-implementation-plan.md)
    por: usuario
    em: "2026-11-04"
    evidencia: "comentário do usuário na issue 31, 2026-11-04: 'plano do arredondamento aprovado'"
autorizacoes_vigentes: []
proximo_passo: A3 da entrega
pendencias: []
```

Checks em 2026-11-05, no commit 81bd0e2:
- `python -m unittest discover -s tests`: 12 testes OK.
- `ruff check .`: sem achados.

Nota de 2026-11-06, escrita pelo usuário: a Ana mergeou na `main` uma mudança em `src/precos.py` (troca do tipo float por Decimal). A branch foi atualizada com a `main` hoje, e o commit atual é 9c3e7d4.
