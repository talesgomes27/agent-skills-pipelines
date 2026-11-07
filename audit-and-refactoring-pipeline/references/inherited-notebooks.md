# Notebooks herdados

Para reconhecer uma pasta de notebooks, dados e scripts que ninguém sabe rodar, antes de mudar qualquer coisa. O trabalho fica no modo de reconhecimento ou de auditoria sem edição.

## Mapa sem executar

- Se a pasta não é um repositório Git, diga isso e não crie um sem autorização; o estado do trabalho vai na resposta.
- Liste notebooks, scripts, dados e saídas, com data de modificação, tamanho e hash. Ler datas e calcular hash é inspeção e não executa nada.
- Leia primeiro o script que gera o relatório recorrente: para onde ele grava ou envia, caminhos fixos e credenciais no código.
- Para cada notebook, extraia lendo o código, sem rodar, o que ele lê e grava: caminhos de arquivo, tabelas, `%run` e imports de módulos locais. Com muitos notebooks, busque essas chamadas (`read_csv`, `to_csv`, `open(`, `%run`, caminhos) em vez de ler célula por célula. Contagens de execução fora de ordem nos metadados mostram que o notebook foi rodado fora da sequência das células. Monte a tabela notebook → entradas → saídas e tire dela a ordem provável. Ciclos e entradas que nenhum notebook gera são achados.
- Para cada CSV, diga qual notebook o gera ou se ele vem de fora, com data e hash. Dado sem origem conhecida é achado.
- Procure dados pessoais nas saídas já gravadas e nos CSVs e diga onde estão, sem copiar os valores, seguindo a skill `personal-data`.
- Reconstrua o ambiente como proposta, pelas versões que aparecem nos imports, nos outputs e nos metadados dos notebooks, sem instalar nada.

## Execução isolada

- Só com autorização: numa cópia da pasta, com a rede bloqueada, as escritas indo para a cópia e sem credenciais. Criar o ambiente descartável para isso também pede autorização.
- Rode na ordem do mapa, um notebook por vez, com um executor como nbclient ou papermill, e registre o que falha e onde. Notebook que tenta rede, envio ou escrita fora da cópia é parado e vira achado.

## Entrega

- O mapa da ordem e a tabela de entradas e saídas.
- Três listas, cada item com a evidência: o que funciona; o que está quebrado, com o erro; o que é arriscado, como dados pessoais, credenciais no código, efeitos externos e resultados que dependem da ordem das células.
- À parte, o que não foi possível verificar e por quê.

Os itens quebrados e arriscados entram também na tabela de achados do Gate 2. Como o pedido é entender antes de mexer, a coluna de sugestão traz o próximo passo, como confirmar a origem de um CSV ou isolar uma credencial, e não uma refatoração. A lista do que funciona fica só na entrega.
