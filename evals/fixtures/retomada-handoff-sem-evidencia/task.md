```yaml
pipeline: release-and-ops-pipeline
gate: RL-4
estado: em_andamento
execucao: preparado
modo: por-efeito
esforco: padrao
aprovacoes:
  - item: plano da release 1.3.0
    por: usuario
    em: "2026-11-05"
    evidencia: "aprovação do usuário no PR 18, 2026-11-05: 'plano da 1.3.0 ok'"
autorizacoes_vigentes:
  - efeito: deploy em produção
    destino: Posit Connect da empresa
    por: agente
    em: "2026-11-06"
    evidencia: ""
    vale_ate: fim da tarefa
proximo_passo: publicar no Posit Connect e rodar o smoke
pendencias: []
```

Artefato: bundle do commit 2d71aa0, checks OK em 2026-11-06.
