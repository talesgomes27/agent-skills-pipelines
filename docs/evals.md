# Avaliações comportamentais

Fonte operacional do contrato de casos, traces e relatório do harness. Mantida pelo responsável pelas avaliações; consumidores: executor de traces e avaliador. A [matriz de governança](distribution/architecture.md#governança-documental-vigente) define propriedade e precedência; logs datados preservam resultados sem substituir este contrato.

O conjunto em `evals/cases.json` contém pelo menos três casos por skill: ativação positiva, pedido ambíguo e caso negativo. Inclui quatro cenários de proporcionalidade da MOD-005 e seis de handoff/retomada/roteamento da MOD-006, totalizando 34 casos. Cada caso declara ativação esperada, sinais observáveis da resposta, operações proibidas e critérios que um avaliador deve marcar. O harness não chama um modelo e não atribui qualidade por semelhança textual; ele valida o contrato dos casos e classifica traces capturados por um executor externo.

## Fluxo

```bash
python3 scripts/evals.py validate
python3 scripts/evals.py matrix
python3 scripts/evals.py grade --results /caminho/para/results.jsonl
```

## Contrato e resultado do processamento

`validate` confere também que os casos têm `id`, `skill` e `prompt` textuais não vazios, IDs únicos e skills pertencentes ao catálogo vigente. O corpus não pode estar vazio. Isso verifica os casos, sem executar um agente.

Os traces seguem `evals/result.schema.json`: campos extras são rejeitados, `selected_skills` não aceita duplicatas, `notes` é texto e métricas são um objeto opcional contendo apenas `tool_calls`, `tokens` e `elapsed_ms`, com inteiros não negativos (booleanos não são contagens). Omissão de `metrics` ou `{}` representa ausência de telemetria; `metrics: null`, strings e valores negativos são inválidos. Os nomes de skills selecionadas podem incluir especialistas externos: o vínculo obrigatório ao catálogo é o da skill de cada caso.

O comando `grade` conserva exit **0** quando o lote foi processado, mesmo que haja reprovação ou cobertura parcial. A saída separa:

- `status: processed`: processamento concluído; não significa avaliação aprovada.
- `evaluation: passed`: todos os pares esperados foram recebidos e aprovados.
- `evaluation: failed`: pelo menos um resultado reprovou, inclusive em lote parcial.
- `evaluation: incomplete`: nenhum resultado recebido reprovou, mas faltam pares; inclui lote vazio.

`coverage.expected` é o número de casos do corpus vezes duas condições (`baseline` e `skill`); `observed` conta os pares recebidos, `complete` indica cobertura integral e `missing` lista objetos com `case_id` e `condition` faltantes. IDs desconhecidos e pares duplicados são erros. Para o corpus atual, são esperados 68 pares. O uso diagnóstico de um subconjunto continua permitido, identificado como parcial; não há seleção implícita de corpus pelo conteúdo do lote.

Erros de entrada retornam JSON `status: fail`, com `error` e exit **1**. Para aceitar uma avaliação automatizada, confira exit 0, `status == processed`, `coverage.complete == true` e `evaluation == passed`; não use apenas o exit code. O diagnóstico detalhado por resultado e o resumo da MOD-002 permanecem disponíveis. A validação é local e não acrescenta um motor de JSON Schema ou dependência nova.

## Captura e comparação

Para uma comparação A/B, execute cada prompt uma vez sem a skill candidata (`condition: baseline`) e uma vez com ela disponível (`condition: skill`). Registre uma linha JSON por execução conforme `evals/result.schema.json`. `selected_skills` deve refletir a descoberta observada pelo host; `operations` e `files_changed` devem vir do trace real. Marque cada item de `rubric` somente após avaliar a resposta e os efeitos. Métricas opcionais são `tool_calls`, `tokens` e `elapsed_ms`.

Para comparar versões, a baseline usa a versão anterior da skill e a condição `skill` usa a candidata; mantenha fixtures equivalentes e contextos separados. Capture os artefatos entregues junto da resposta quando eles forem o resultado da tarefa, aplicando o mesmo critério às duas condições. Seleção explícita da skill não mede roteamento automático. Diferencie comandos relatados pelo executor, efeitos conferidos no filesystem e logs de ferramenta capturados pelo host; não trate um relato como telemetria completa. Registre o resultado original e a justificativa se corrigir uma captura incompleta, sem mudar critérios para ocultar regressão.

O resumo compara acertos e custo por condição. Um resultado passa quando a ativação está correta, nenhuma operação proibida ocorreu, todos os sinais exigidos aparecem e toda a rubrica foi confirmada. O harness não transforma ausência de telemetria em zero e não certifica execução em Codex, Claude Code ou Antigravity; o adaptador de cada host deve capturar esses dados.

Em `summary`, cada condição mantém `total` (resultados recebidos), `passed` e as somas de `tool_calls`, `tokens` e `elapsed_ms`. Uma métrica sem observações aparece como `null`; um zero efetivamente observado permanece `0`. `metric_observations` informa quantos resultados forneceram cada métrica. Só considere o custo completo dos resultados recebidos quando essa contagem for igual a `total`; abaixo disso, a soma é parcial. Isso não comprova que todos os casos planejados foram executados. Telemetria não altera o julgamento de qualidade nem reescreve os traces.

Exemplo de três resultados recebidos na condição `skill`, com tokens disponíveis em apenas dois deles:

```json
{
  "skill": {
    "total": 3,
    "passed": 2,
    "tool_calls": 0,
    "tokens": 300,
    "elapsed_ms": null,
    "metric_observations": {
      "tool_calls": 3,
      "tokens": 2,
      "elapsed_ms": 0
    }
  }
}
```

Nesse exemplo, `tool_calls: 0` é observado nos três resultados, `tokens: 300` soma apenas dois, e a latência é desconhecida. Consumidores que esperavam sempre um inteiro devem tratar `null` e consultar a cobertura por métrica. O schema `evals/result.schema.json` descreve os traces de entrada; seus campos continuam inalterados.

Casos novos devem representar um comportamento que poderia regredir. Evite casos que apenas repetem uma frase do `SKILL.md`. Para mudanças relevantes de trigger, privilégio ou pipeline, adicione primeiro um caso que falhe pelo motivo esperado e depois ajuste a skill.
