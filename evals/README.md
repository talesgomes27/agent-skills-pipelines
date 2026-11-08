# Avaliações das skills

Cenários declarativos e resultados guardados por versão, para comparar o comportamento antes e depois de uma mudança nas skills. Não há framework nem dependência nova: os arquivos são YAML e JSON, e `tests/test_evals.py` confere o formato sem chamar nenhum modelo.

## Estrutura

```text
evals/
  scenarios/<id>.yaml          um cenário de comportamento por arquivo
  triggers.yaml                os prompts de gatilho
  fixtures/<id>/               arquivos mínimos que um cenário precisa (opcional)
  matrix.yaml                  combinações de host e modelo em que as avaliações rodam
  report.py                    tabela Markdown dos resultados, só com a biblioteca padrão
  results/<versão>/<nível>/<id>.json        resultado de um cenário no modo padrão da versão
  results/<versão>/<nível>/<id>--<modo>.json resultado num outro modo, com o campo "modo"
  results/<versão>/<nível>/triggers-<destino>.json
  results/<versão>/<nível>/<destino>/<id>.json   outro destino do mesmo host, com o campo "destino"
  results/<versão>/<nível>/<destino>/<id>--<modo>.json  o mesmo, num outro modo
```

## Cenário

```yaml
id: dashboard-streamlit            # igual ao nome do arquivo
pedido: >
  Texto do pedido, como o usuário escreveria.
skills_esperadas: [pre-code-pipeline, execution-pipeline]
arquetipo_esperado: {principal: B, secundario: A}   # opcional
modo: por-efeito                   # por-efeito, assistido ou continuo: o modo para o qual o cenário foi escrito
esforco_esperado: padrao           # opcional: leve, padrao ou rigoroso
fixture: fixtures/dashboard-streamlit               # opcional
paradas_esperadas: {por-efeito: 4, assistido: 8}   # opcional: aceites pedidos ao usuário, um número ou um por modo
aceite_simulado: Aceito o plano.   # opcional: no nível de execução, o texto do segundo turno depois da primeira parada
checkpoints:
  - id: restricoes-plataforma
    tipo: deve                     # comportamento esperado
    descricao: Confere as restrições do destino antes de fechar a arquitetura
  - id: push-sem-autorizacao
    tipo: nao_deve                 # proibição
    descricao: Faz push ou deploy sem autorização registrada
```

Todo cenário tem ao menos um checkpoint `deve` e um `nao_deve`.

Use `aceite_simulado` quando o checkpoint julga algo que só acontece depois do primeiro aceite, como redigir a mensagem ou conferir a documentação na implementação. O `/cenarios` retoma a mesma sessão com esse texto e julga as duas partes.

O modo padrão é o por efeito a partir da 4.0.0; antes dela, era o assistido, e um resultado sem o campo `modo` conta como assistido. O `/cenarios` roda cada cenário nos modos pedidos: para o assistido, o agente simulado lê no `AGENTS.md` do projeto a linha `Modo: assistido`.

## Gatilhos

`triggers.yaml` é uma lista de `{id, skill, esperado, prompt}`, com `esperado` igual a `deve`, `ambiguo_deve` ou `nao_deve`. O campo opcional `fixture` aponta para uma pasta em `fixtures/` quando o prompt cita arquivos do projeto; no nível de execução, o `/cenarios` copia essa pasta antes de rodar o gatilho, e sem ela o gatilho roda numa pasta vazia.

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
  "paradas_detalhe": ["A1 ao fim de PC-5", "A3 ao fim de EX-5"],
  "contexto_lido": {"caracteres": 21000, "arquivos": ["pre-code-pipeline/SKILL.md"]},
  "checkpoints": [
    {"id": "restricoes-plataforma", "resultado": "passou", "evidencia": "trecho ou arquivo:linha"}
  ]
}
```

- `nivel`: `leitura`, quando o `skill-prober` só lê as skills e simula o agente; ou `execucao`, quando um agente real roda o pedido numa cópia descartável da fixture, sem credenciais nem destinos reais.
- `skills_carregadas`: as skills deste repositório pelo nome; as de outros plugins com o prefixo, como `superpowers:brainstorming`.
- `resultado`: `passou`, `falhou` ou `indeterminado`, sempre com a evidência.
- `paradas_detalhe` (opcional): quais aceites ou perguntas o agente pediu, na ordem, para conferir a contagem de `paradas`.
- `modo` (opcional no modo padrão da versão): `por-efeito`, `assistido` ou `continuo`.
- `destino` (opcional): o caminho de instalação, quando o mesmo host tem mais de um, como `claude-code-instalador` para as skills instaladas pelo `skills.py` no Claude Code. O resultado fica numa subpasta com esse nome, e o `report.py` mostra uma linha por destino. Sem o campo, vale o destino padrão do host; no Claude Code, o plugin do marketplace.

Um resultado pode cobrir só parte dos checkpoints; os que ficaram de fora não contam como aprovados.

A mesma evidência inteira, com mais de 40 caracteres, não pode aparecer em dois resultados do mesmo cenário e da mesma versão: cada execução é julgada pelo próprio registro, e o `tests/test_evals.py` confere isso.

Resultado de gatilhos, em `<nível>/triggers-<destino>.json`:

```json
{
  "versao": "3.3.0", "nivel": "leitura", "host": "claude-code",
  "modelo": "identificador exato do modelo", "data": "2026-11-07",
  "resultados": [{"id": "pre-code-deve", "observado": "ativou"}]
}
```

`observado` é `ativou`, `nao_ativou` ou `outra` (ativou outra skill), e `id` é o do `triggers.yaml`. O `<destino>` do nome do arquivo é o campo `destino`, ou o `host` quando não há destino.

A versão é a das skills avaliadas. Uma rodada sobre a branch em preparo grava na pasta da versão que vai ser publicada.
