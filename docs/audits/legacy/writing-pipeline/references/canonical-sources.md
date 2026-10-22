# Manifesto Canônico de Fontes

Fontes autorizadas para citação formal via `[@chave]` no âmbito da
skill `writing-pipeline`. Toda chave aqui listada é considerada
válida pelo verificador anti-alucinação.

## Livros

### [@zinsser_1976]
- **Autor**: William Zinsser
- **Obra**: On Writing Well
- **Ano**: 1976
- **Escopo**: Clareza expositiva, eliminação de palavras supérfluas.
- **Uso recomendado**: Parágrafos introdutórios, revisão de prosa
  técnica, corte de redundância.

### [@williams_1981]
- **Autor**: Joseph M. Williams
- **Obra**: Style: Lessons in Clarity and Grace
- **Ano**: 1981
- **Escopo**: Coesão sujeito-verbo, fluxo temático entre frases.
- **Uso recomendado**: Estruturação de parágrafos argumentativos.

### [@pinker_2014]
- **Autor**: Steven Pinker
- **Obra**: The Sense of Style
- **Ano**: 2014
- **Escopo**: Prosa clássica, maldição do conhecimento, clareza
  técnica.
- **Uso recomendado**: Explicações complexas para público não-técnico.

### [@knaflic_2015]
- **Autor**: Cole Nussbaumer Knaflic
- **Obra**: Storytelling with Data
- **Ano**: 2015
- **Escopo**: Integração texto-dataviz, carga cognitiva.
- **Uso recomendado**: Relatórios Quarto, seções de resultados.

### [@squarisi_2005]
- **Autor**: Dad Squarisi
- **Obra**: Escrever Bem
- **Ano**: 2005
- **Escopo**: Concisão, pontuação e eliminação de chavões em PT-BR.
- **Uso recomendado**: Revisão de prosa técnica em português.

## Guias e Normas

### [@google_style]
- **Fonte**: Google Developer Documentation Style Guide
- **URL**: https://developers.google.com/style
- **Escopo**: Voz ativa, presente do indicativo, padronização de
  comandos e APIs.
- **Uso recomendado**: READMEs de software, documentação de API.

### [@microsoft_style]
- **Fonte**: Microsoft Writing Style Guide
- **URL**: https://learn.microsoft.com/style-guide/
- **Escopo**: Tom conversacional, clareza em mensagens de erro.
- **Uso recomendado**: Tutoriais, guias de início rápido.

### [@apa_7th]
- **Fonte**: APA 7th Edition
- **Escopo**: Citações autor-data em relatórios de pesquisa.
- **Uso recomendado**: Arquétipo A, seções de método e resultados.

### [@abnt_10520]
- **Fonte**: ABNT NBR 10520
- **Escopo**: Citações em documentos técnicos e acadêmicos em PT-BR.
- **Uso recomendado**: Arquétipo A em português.

## Como Adicionar Novas Fontes

1. Editar este arquivo adicionando uma seção nova com chave única.
2. A chave deve seguir o padrão `<autor>_<ano>` ou `<fonte>_<ano>`.
3. Atualizar o commit referenciando a fonte adicionada.
4. Nunca reutilizar chaves. Chaves são imutáveis.

## Como Usar no Texto

Citação formal:
  Segundo [@zinsser_1976], a clareza exige cortes implacáveis.

Link inline (fonte fora do manifesto):
  Ver [Pinker, 2014](https://example.com/sense-of-style).

Proibido:
  [@pinker_sense_style] (chave não registrada acima).
