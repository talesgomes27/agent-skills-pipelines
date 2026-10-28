# Preparação autorizada da CI candidata

Autorização: pedido de 28/10/2026, preparação/commit/push exclusivamente de codex/meta-skills-2-candidate em talesgomes27/agent-skills-pipelines. Base 33b773cf099c6be3183526b31b758d783260cbd1. Etapa remota planejada; resultado ainda não inferido neste documento anterior ao commit.

## Escopo exato

Overlay em distribution/catalog.json e README.md. Ajuste mínimo .github/workflows/ci.yml: fetch-depth:0 somente no checkout da matriz de testes; job somente de link mantém checkout padrão. Os testes MOD-007/008 dependem de b9b9469, 10b14ad e bc41c7e. Buscar somente esses commits seria alternativa, mas adicionaria comandos/refs e manutenção; profundidade fixa não garante ancestralidade suficiente. O repositório é pequeno; histórico completo evita skips de preparação e preserva ações/OS/Python/permissões existentes.

Adicionar 1.0 à lista de entradas rejeitadas do teste de métricas existente (tests/test_evals.py). Nenhuma normalização no runtime, mudança de schema de entrada ou afrouxamento de teste. Conteúdo candidato adicional: este documento, README, API, COMPATIBILITY, RELEASE-NOTES, SECURITY/security.json, schema-matrix.json, contracts/grade-output.schema.json e evaluations-v2/PROTOCOL.md/proposal.json.

Matriz: ubuntu/windows/macos-latest × Python 3.9/3.14; job link Linux/Python3.14. Unitários esperados: 53; informar skips por SO se ocorrerem, sem contá-los como execução. Doctor cobre oito skills; instalação copy/link da CI exclui humanizer por configuração preexistente, logo cobre sete. A preparação local testou oito. Validação de casos é estrutural; não executa modelos nem aprova qualidade. O job link não contém suíte unitária própria.

Actions permanecem nos SHAs aprovados; contents:read é a única permissão declarada; nenhum secrets, environment, publish, deploy, registry ou escrita externa acrescentados. Setup instala somente requirements.txt de runtime. CI não executa a validação formal adicional com jsonschema nem o tar local; tais resultados são evidência local delimitada.

## Integridade e isolamento

Sem git add .; staging por lista de arquivos revisada. Nenhum artefato .gz ou cache, task.md principal, pasta delegation ou teste DEL no novo commit. O push incluirá também os oito commits MOD locais ancestrais desde main remota 869444d; isso é necessário à base autorizada 33b773c e ao histórico da CI. Inspecionar todo o intervalo enviado, não apenas o último diff. Nenhuma outra branch ou tag é enviada.

Os artefatos locais prévios conservam sua identidade da base 33b773c com overlay 2.0.0: não incluem o ajuste de CI nem estes documentos atualizados e não devem ser rotulados como build do futuro commit de CI. Reempacotamento final será gate próprio com nova identidade e testes pertinentes.

## Gates posteriores

Consultar run por SHA exato e acompanhar sete jobs terminais. Registrar contagens/falhas/erros/skips a partir dos logs; job verde não prova passo omitido. Falha exige diagnóstico, sem commit/push corretivo automático que amplie escopo. Campanha v2 depende de nova autorização; suas fixtures/controles/revisor ainda exigem congelamento. Merge/tag/publicação e perfis reais continuam proibidos.

## Evidência local anterior ao commit

Em 28/10/2026, Linux/Python 3.14.4: 53 testes unitários passaram, sem skips; doctor das oito skills e validate de casos passaram. MOD-010 reconciliou grades/hashes e 24 replays com as duas falhas esperadas D-review. Três schemas foram conferidos e as 12 comparações schema/CLI reproduziram a matriz preservada. Workflow YAML e semântica da matriz/permissões/SHAs foram validados localmente. Foram examinados 171 blobs dos oito commits MOD que serão enviados, além dos 15 arquivos selecionados, sem achados nos quatro padrões de alta especificidade. Os dois arquivos .tar.gz originais e seus manifests seguem íntegros; não são builds do novo commit. Logs e contagens remotas serão coletados após o push, sem inferência de sucesso.
