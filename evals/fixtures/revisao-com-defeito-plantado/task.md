```yaml
pipeline: execution-pipeline
gate: EX-5
estado: em_andamento
execucao: null
modo: por-efeito
esforco: rigoroso
aprovacoes:
  - item: plano da tabela de pedidos (docs/05-implementation-plan.md)
    por: usuario
    em: "2026-11-04"
    evidencia: "aprovação do usuário no PR 22, 2026-11-04: 'plano aprovado, pode implementar'"
autorizacoes_vigentes: []
proximo_passo: revisão e A3 da entrega
pendencias: []
```

Checks em 2026-11-06, no commit 5e1f0aa:
- `pytest -q`: 2 passed.
- `ruff check .`: sem achados.
