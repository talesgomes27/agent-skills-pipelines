# Arquétipo C: Convenções de Escrita

## Registro e Voz

- Telegráfico, imperativo, operacional.
- 2ª pessoa imperativa ("Execute `app run`...").
- Tom direto, orientado à tarefa, zero prosa.

## Estrutura README

1. Nome do comando + one-liner.
2. Instalação (< 3 linhas).
3. Exemplos de invocação.
4. Tabela de flags/argumentos.
5. Variáveis de ambiente.
6. Exemplos de pipe Unix.

## Mensagens de Erro

Formato POSIX:

  erro: <descrição curta>. <comando sugerido>.

Exemplo:
  erro: arquivo 'config.yaml' não encontrado em /etc/app/.
  Use --config <path> para indicar um arquivo válido.

## Logs Estruturados

- Níveis: DEBUG, INFO, WARNING, ERROR.
- Formato: `<nível> <timestamp> <módulo>: <mensagem>`.

## Comprimento de Frase

Curto: 5–12 palavras. Sem rodeios.

## Citação

Não aplicável. Apenas referências a flags, manpages e padrões POSIX.
