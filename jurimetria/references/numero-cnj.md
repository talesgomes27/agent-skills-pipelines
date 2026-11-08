# Número único de processo

Leia quando o trabalho cruza, conta, valida ou formata números de processo.

## Estrutura

A Resolução CNJ 65/2008 institui a numeração única, com a estrutura `NNNNNNN-DD.AAAA.J.TR.OOOO` e seis campos obrigatórios (art. 1º):

| Campo | Dígitos | Significado |
|---|---|---|
| NNNNNNN | 7 | Sequencial por unidade de origem, reiniciado a cada ano; zeros à esquerda podem ser omitidos. Na Justiça Estadual e do DF, o sequencial pode ser vinculado ao tribunal em vez da origem (§ 1º-A). |
| DD | 2 | Dígito verificador, pelo algoritmo Módulo 97 Base 10 da norma ISO 7064:2003 (§ 2º e Anexo VIII). |
| AAAA | 4 | Ano do ajuizamento. |
| J | 1 | Segmento: 1 STF, 2 CNJ, 3 STJ, 4 Justiça Federal, 5 Justiça do Trabalho, 6 Justiça Eleitoral, 7 Justiça Militar da União, 8 Justiça dos Estados e do DF e Territórios, 9 Justiça Militar Estadual. |
| TR | 2 | Tribunal dentro do segmento. Nos tribunais de justiça, 01 a 27 pela ordem alfabética dos Estados e do DF; o TJ do Pará é `8.14`. Zero nos processos originários de STF, CNJ, STJ, TST, TSE e STM. |
| OOOO | 4 | Unidade de origem. No 1º grau, 0001 a 8999 (na Justiça Estadual, o foro de tramitação); 0000 nos processos originários dos tribunais; primeiro algarismo 9 nas turmas recursais. Cada tribunal publica a tabela das suas unidades. |

O número não se repete nem é reaproveitado, nem em cancelamento de distribuição. A redistribuição para outro tribunal gera número novo; no mesmo tribunal, não; e a execução penal mantém o número mesmo quando muda de tribunal (arts. 3º e 5º, com a redação da Resolução 223/2016). O recurso julgado por tribunal de outro segmento nos próprios autos recebe OOOO 9999 (art. 3º, § 3º).

## Dígito verificador (Anexo VIII)

1. Monte a cadeia `NNNNNNN AAAA J TR OOOO 00`, com o sequencial em 7 dígitos e `00` no lugar do dígito.
2. `DD = 98 − (cadeia mod 97)`, escrito em dois dígitos, com zero à esquerda se preciso.
3. Para conferir um número, a cadeia `NNNNNNN AAAA J TR OOOO DD` deixa resto 1 na divisão por 97.

A cadeia tem 20 dígitos e passa do inteiro de 64 bits e da precisão exata de um `double`. Em Python o inteiro não tem limite. Em linguagens sem inteiro grande, use a fatoração do próprio anexo: `R1 = NNNNNNN mod 97`, `R2 = (R1 seguido de AAAA J TR) mod 97`, `R3 = (R2 seguido de OOOO 00) mod 97`, `DD = 98 − R3`.

Exemplos fictícios, calculados por esse algoritmo: `0000100-13.2008.8.14.0000` e `0801234-84.2023.8.14.0301`. A norma diz que "a numeração dos processos constante dos Anexos é fictícia e exemplificativa", e o dígito dos exemplos não confere pelo algoritmo: não os use como teste.

## Ferramentas

- `scripts/numero_cnj.py` (desta skill): `valido()`, `normalizar()`, `partes()`, `formatar()` e `digito()`; pela linha de comando, lê um número por linha ou uma coluna de CSV e separa válidos de inválidos.
- `abjutils`, em R, da Associação Brasileira de Jurimetria: `calc_dig()`, `check_dig()`, `verify_cnj()`, `clean_cnj()`, `build_id()`, `extract_parts()` e `separate_cnj()`.

## Fontes

Conferidas em 08/11/2026:

- Resolução CNJ 65/2008, com as alterações das Resoluções 223/2016 e 477/2022: https://atos.cnj.jus.br/atos/detalhar/119
- Texto compilado com os anexos I a VIII: https://atos.cnj.jus.br/files/compilado23285720221017634de539229ab.pdf
- abjutils no CRAN: https://cran.r-project.org/package=abjutils
