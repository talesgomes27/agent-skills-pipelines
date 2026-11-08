```yaml
pipeline: execution-pipeline
gate: EX-3
estado: em_andamento
execucao: null
modo: por-efeito
esforco: padrao
aprovacoes:
  - item: plano do filtro por região (docs/05-implementation-plan.md)
    por: usuario
    em: "2026-11-05"
    evidencia: "aprovação no PR 7: 'plano ok, pode implementar'"
autorizacoes_vigentes: []
proximo_passo: EX-3, tabela exportável em CSV; depois EX-4 e EX-5
pendencias: []
```

Objetivo: filtro por região no relatório de vendas.

Checks em 2026-11-05, no commit 4f2a9c1:
- `python -m unittest discover -s tests`: 6 testes OK.

Base: branch `feat/filtro-regiao`, criada da `main` em 4f2a9c1. Desde então, nem a branch nem a `main` mudaram.
