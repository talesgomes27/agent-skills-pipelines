# Saneamento do conteúdo a publicar

## Escopo e arquivos

Inspecione o conjunto pretendido de commit, pacote, imagem ou site, incluindo outputs e arquivos ignorados que possam entrar por outro processo de build/upload. `.gitignore` não retira arquivos já rastreados nem controla sozinho conteúdo de wheel, container ou artefato publicado.
Preserve dados/fixtures públicos e necessários; não bloqueie toda extensão CSV/Parquet/modelo por regra universal. Defina caminhos e exceções explícitos conforme sensibilidade, licença, tamanho e reprodutibilidade do projeto. Não remova dados rastreados ou reescreva histórico como efeito de uma revisão.
Confira tamanho no conjunto enviado e, quando necessário, no intervalo de histórico pertinente. Limites vêm do host/registry/política; 50 MB não é um teto universal. Scanner de diretório com profundidade fixa não comprova quais blobs serão enviados.

## Segredos, notebooks e saídas

Use scanner já configurado ou inspeção delimitada, sem imprimir valores de credenciais. Diferencie achado, ausência de achados no escopo e falha de execução. Um grep por nomes de variáveis não certifica ausência de segredo e pode imprimir o próprio segredo.
Inclua diffs, arquivos rastreados pertinentes, outputs de notebooks, HTML, bundles JS, logs e caches exportados, conforme o artefato. Dados brutos ignorados podem reaparecer em uma tabela ou snapshot renderizado.
Se houver credencial exposta, bloqueie sua publicação e informe o local sem o valor. Rotação e limpeza de histórico requerem plano e autorização próprios; remover uma linha não invalida um token já divulgado.

## Lockfiles e build

Use verificações do gerenciador real. Em uv, `uv lock --check` verifica atualidade; `uv sync --locked` recusa lock desatualizado em vez de atualizá-lo. `--frozen` usa o lock sem conferir sua atualidade, portanto não prova sincronia por si só. Em outros gerenciadores, confira a opção de instalação imutável correspondente à versão instalada.
Lockfile reproduz dependências apenas nas condições que representa; confirme runtime, plataforma e inputs externos pertinentes. Não atualize dependências ou resolva vulnerabilidade por migração ampla na fase de release sem escopo autorizado.

## Quarto e grafos

`_freeze/` pode conter resultados sensíveis e referências a arquivos; só versione/publique quando a estratégia precisar e o conteúdo estiver revisado. `.quarto/` costuma ser cache local; preserve a política do projeto em vez de apagar diretórios indiscriminadamente.
Verifique freshness de dados e outputs usados no site. `freeze: auto` não detecta toda mudança externa. Um gráfico ou grafo pode expor estrutura/nome de arquivo interno; publicar somente o artefato solicitado e revisado.
Instalar browser, pacote ou extensão exige necessidade técnica e permissões do ambiente; não faça instalação global como pré-requisito universal de um site HTML.
