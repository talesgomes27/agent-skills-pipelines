# Arquétipo B: Convenções de Escrita

## Registro e Voz

- Técnico-descritivo, contratual, normativo.
- 3ª pessoa neutra ("A função retorna...").
- Tom pragmático, focado em contratos e exceções.

## Estrutura README

1. Nome + one-liner (o que faz, para quem).
2. Quick start (< 5 min).
3. Arquitetura e componentes.
4. Variáveis de ambiente.
5. Guia de deploy.

## Docstrings

Formato Google Style:
  def foo(x: int) -> str:
      """Resumo em uma linha.

      Args:
          x: Descrição.

      Returns:
          Descrição.

      Raises:
          ValueError: Descrição.
      """

## OpenAPI / Swagger

- Documentar endpoints com schemas completos.
- Exemplos de request e response.
- Versionamento explícito.

## ADRs

- Título: "ADR-001: Escolha do banco de dados".
- Seções: Contexto, Decisão, Alternativas descartadas, Consequências.

## Comprimento de Frase

Médio: 10–18 palavras. Foco em clareza.

## Citação

Links diretos para RFCs, repositórios, docs oficiais. Sem citação
autor-data.
