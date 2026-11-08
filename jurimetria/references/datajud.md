# API Pública do DataJud

Leia quando o trabalho busca metadados de processos no DataJud, a Base Nacional de Dados do Poder Judiciário, mantida pelo CNJ.

## Como pedir

- Endereço por tribunal: `https://api-publica.datajud.cnj.jus.br/api_publica_<sigla>/_search`, por exemplo `api_publica_tjpa`. A lista de siglas está na página de endpoints da wiki; confira lá o tribunal antes de montar a coleta.
- Método `POST`, com `Content-Type: application/json` e o corpo na Query DSL do Elasticsearch, como `{"query": {"match": {"numeroProcesso": "<20 dígitos>"}}}` ou combinações com `bool` e `must`. A API aceita também agregações.
- Autenticação no cabeçalho `Authorization: APIKey <chave pública>`. A chave vigente fica na página de acesso da wiki, e o CNJ pode trocá-la a qualquer momento: leia-a de lá e guarde-a na configuração do projeto.
- O número do processo vai sem máscara, com 20 dígitos.

## Paginação e limites

- O padrão é 10 registros por resposta, e `size` vai de 10 a 10.000.
- Para mais que isso, use `search_after`: ordene por `@timestamp` e passe o valor de `sort` do último documento na consulta seguinte.
- O termo de uso limita a 120 requisições por minuto sem autorização escrita, e o CNJ pode limitar o acesso sem aviso. Ponha pausa e repetição com espera no código, e registre quantas páginas vieram.

## O que vem e o que não vem

- Campos do glossário: `numeroProcesso`, `tribunal`, `grau`, `dataAjuizamento`, `nivelSigilo`, `classe` (código e nome, pela TPU), `assuntos`, `orgaoJulgador` (com o código IBGE do município), `movimentos` (código, nome, data e hora e complementos tabelados), `formato`, `sistema` e campos de controle como `@timestamp`.
- Não vêm partes, advogados, valor da causa nem o inteiro teor de decisões. A norma prevê os polos quando são pessoas jurídicas, mas o glossário ainda não mostra esse campo; confira antes de contar com ele.
- Processos em segredo de justiça têm os dados excluídos ou anonimizados (Portaria CNJ 160/2020, art. 3º, com a redação da Portaria 374/2026). Filtre também `nivelSigilo` acima de zero e relate quantos saíram.
- Os dados refletem as remessas de cada tribunal, sem garantia do CNJ de precisão ou atualidade. A API está em fase beta.

## Termos de uso

- Uso só para fins legais, não comerciais e autorizados; sem modificar, distribuir, vender ou explorar comercialmente os dados.
- Citar o CNJ e o DataJud como fontes é obrigatório (Portaria 160/2020, art. 4º, com a redação de 2026). O termo pede também dar ciência ao CNJ de estudo ou relatório publicado e não coletar informações pessoais de terceiros.
- O aceite é tácito, pelo uso: mostre os termos ao usuário no plano, antes da primeira coleta.

## Fontes

Conferidas em 08/11/2026:

- Wiki da API Pública: https://datajud-wiki.cnj.jus.br/api-publica/ (acesso, endpoints, exemplos, glossário e considerações finais)
- Portaria CNJ 160/2020, texto compilado: https://atos.cnj.jus.br/atos/detalhar/3453
- Portaria CNJ 374/2026: https://atos.cnj.jus.br/atos/detalhar/6972
- Termo de uso v1.2: https://formularios.cnj.jus.br/wp-content/uploads/2023/11/Termos-de-uso-api-publica-V1.2.pdf
