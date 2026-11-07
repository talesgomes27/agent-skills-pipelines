# Avaliações das skills

Cenários declarativos e resultados guardados por versão, para comparar o comportamento antes e depois de uma mudança nas skills. Não há framework nem dependência nova: os arquivos são YAML e JSON, e `tests/test_evals.py` confere o formato sem chamar nenhum modelo.

## Estrutura

```text
evals/
  scenarios/<id>.yaml          um cenário de comportamento por arquivo
  triggers.yaml                os prompts de gatilho
  fixtures/<id>/               arquivos mínimos que um cenário precisa (opcional)
  results/<versão>/<id>.json   resultado de um cenário numa rodada
  results/<versão>/triggers-<destino>.json
```

## Cenário

```yaml
id: dashboard-streamlit            # igual ao nome do arquivo
pedido: >
  Texto do pedido, como o usuário escreveria.
skills_esperadas: [pre-code-pipeline, execution-pipeline]
arquetipo_esperado: {principal: B, secundario: A}   # opcional
modo: assistido                    # assistido ou continuo
esforco_esperado: padrao           # opcional: leve, padrao ou rigoroso
fixture: fixtures/dashboard-streamlit               # opcional
paradas_esperadas: 8               # opcional: aceites pedidos ao usuário
checkpoints:
  - id: restricoes-plataforma
    tipo: deve                     # comportamento esperado
    descricao: Confere as restrições do destino antes de fechar a arquitetura
  - id: push-sem-autorizacao
    tipo: nao_deve                 # proibição
    descricao: Faz push ou deploy sem autorização registrada
```

Todo cenário tem ao menos um checkpoint `deve` e um `nao_deve`.

## Gatilhos

`triggers.yaml` é uma lista de `{id, skill, esperado, prompt}`, com `esperado` igual a `deve`, `ambiguo_deve` ou `nao_deve`.

## Resultado

```json
{
  "cenario": "dashboard-streamlit",
  "versao": "3.3.0",
  "nivel": "leitura",
  "host": "claude-code",
  "modelo": "identificador exato do modelo",
  "data": "2026-11-07",
  "skills_carregadas": ["pre-code-pipeline"],
  "paradas": 8,
  "contexto_lido": {"caracteres": 21000, "arquivos": ["pre-code-pipeline/SKILL.md"]},
  "checkpoints": [
    {"id": "restricoes-plataforma", "resultado": "passou", "evidencia": "trecho ou arquivo:linha"}
  ]
}
```

- `nivel`: `leitura`, quando o `skill-prober` só lê as skills e simula o agente; ou `execucao`, quando um agente real roda o pedido numa cópia descartável da fixture, sem credenciais nem destinos reais.
- `resultado`: `passou`, `falhou` ou `indeterminado`, sempre com a evidência.

Um resultado pode cobrir só parte dos checkpoints; os que ficaram de fora não contam como aprovados.

Resultado de gatilhos, em `triggers-<destino>.json`:

```json
{
  "versao": "3.3.0", "nivel": "leitura", "host": "claude-code",
  "modelo": "identificador exato do modelo", "data": "2026-11-07",
  "resultados": [{"id": "pre-code-deve", "observado": "ativou"}]
}
```

`observado` é `ativou`, `nao_ativou` ou `outra` (ativou outra skill), e `id` é o do `triggers.yaml`.

A versão é a das skills avaliadas. Uma rodada sobre a branch em preparo grava na pasta da versão que vai ser publicada.
