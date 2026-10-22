# Avaliações comportamentais

O conjunto em `evals/cases.json` contém três casos por skill: ativação positiva, pedido ambíguo e caso negativo. Cada caso declara ativação esperada, sinais observáveis da resposta, operações proibidas e critérios que um avaliador deve marcar. O harness não chama um modelo e não atribui qualidade por semelhança textual; ele valida o contrato dos casos e classifica traces capturados por um executor externo.

## Fluxo

```bash
python3 scripts/evals.py validate
python3 scripts/evals.py matrix
python3 scripts/evals.py grade --results /caminho/para/results.jsonl
```

Para uma comparação A/B, execute cada prompt uma vez sem a skill candidata (`condition: baseline`) e uma vez com ela disponível (`condition: skill`). Registre uma linha JSON por execução conforme `evals/result.schema.json`. `selected_skills` deve refletir a descoberta observada pelo host; `operations` e `files_changed` devem vir do trace real. Marque cada item de `rubric` somente após avaliar a resposta e os efeitos. Métricas opcionais são `tool_calls`, `tokens` e `elapsed_ms`.

O resumo compara acertos e custo por condição. Um resultado passa quando a ativação está correta, nenhuma operação proibida ocorreu, todos os sinais exigidos aparecem e toda a rubrica foi confirmada. O harness não transforma ausência de telemetria em zero e não certifica execução em Codex, Claude Code ou Antigravity; o adaptador de cada host deve capturar esses dados.

Casos novos devem representar um comportamento que poderia regredir. Evite casos que apenas repetem uma frase do `SKILL.md`. Para mudanças relevantes de trigger, privilégio ou pipeline, adicione primeiro um caso que falhe pelo motivo esperado e depois ajuste a skill.
