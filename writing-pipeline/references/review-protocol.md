# Protocolo de Revisão Não-Destrutiva

Padrão adotado: **Original → Sugestão → Racional**.

A skill NÃO reescreve o conteúdo. Ela produz uma tabela com sugestões
que o autor humano aceita ou rejeita.

## Formato

| Linha | Original | Sugestão | Racional |
|:---:|:---|:---|:---|
| 42 | "orquestração perfeita entre resiliência e performance" | "combinação de retries com timeout de 400ms" | Adjetivos de marketing; substituir por fatos técnicos. |
| 58 | "não apenas escalável, mas também robusto" | "suporta 2.500 tx/s com SLA de 99,9%" | Falso contraste; substituir por números. |

## Categorias Verificadas

1. **Fatos técnicos**: valores, APIs, comandos, paths.
2. **Gramática e pontuação**.
3. **Consistência de terminologia** (ex.: "callback" vs "callback
   function").
4. **Estrutura e ordem** de seções.
5. **Tom e registro** aderente ao arquétipo.
6. **Citações e referências** contra manifesto canônico.

## Regras

- Nunca reescrever sem listar o motivo.
- Nunca alterar termos técnicos por preferência estilística.
- Nunca silenciar erros factuais; reportar e aguardar decisão.
