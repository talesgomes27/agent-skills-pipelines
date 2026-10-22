# Revisão sem alterar o alvo

Use no Modo 2. Leia o trecho e somente as fontes necessárias às alegações materiais. Preserve o arquivo original; produzir um relatório no destino solicitado não concede autorização para editar o alvo.

## Formato de achados

Quando outra pipeline fornecer colunas, preserve-as. Para auditoria e refatoração, mantenha:

| ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico |
|---|---|---|---|---|---|

Em revisão editorial isolada, pode usar `Localização | Original | Sugestão | Racional`. Use linha verificada, seção ou âncora estável e excerto curto. Não invente linha em documento sem numeração.

## Julgamento

- Separe erro factual, inconsistência de fonte, significado alterado, problema estrutural e preferência de estilo.
- Priorize pelo impacto no leitor e na decisão. Use a escala da pipeline chamadora; P0 não descreve uma preferência lexical. Sem escala fornecida, explique a gravidade em palavras.
- Não transforme um adjetivo em número sem evidência. Exemplo hipotético: diante de “a API é rápida”, a sugestão pode ser retirar a qualificação ou solicitar uma medição, não inventar throughput.
- Preserve termos técnicos corretos, citações, comandos e qualificadores; explique uma alteração material sugerida.
- Não classifique um texto como gerado por IA a partir de contagem de palavras, travessões ou vocabulário.
- Se não houver achados materiais, diga isso e informe somente limitações relevantes. Não fabrique sugestões para preencher a tabela.

## Fechamento

Informe escopo e fontes efetivamente conferidos, achados prioritários e pendências que impeçam aceite. Uma afirmação sem fonte pode ser não verificada sem ser comprovadamente falsa. Não faça reescrita automática, alteração de contratos ou aprovação de gate; aguarde a decisão de quem solicitou a revisão.
