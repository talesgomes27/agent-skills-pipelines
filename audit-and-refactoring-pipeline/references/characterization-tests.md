# Caracterização, mudanças intencionais e recuperação

## O que proteger

Caracterização registra comportamento observado, inclusive comportamentos suspeitos. Ela não decide se o comportamento está correto. Identifique fronteiras e casos relevantes à fatia: retornos, serialização, erros, efeitos em persistência, ordem significativa, recursos e contratos de terminal.
Use testes existentes quando já cobrem esses contratos. Golden Master/snapshot é uma técnica opcional; asserts específicos e testes de integração podem produzir proteção melhor e menor custo. Use runner e diretório de testes compatíveis com o projeto.

## Fixtures e oráculos

- Use dados pequenos representativos dos riscos, não uma quantidade universal de 20–100 linhas. Inclua limites, nulos, duplicatas, datas, grupos e casos de falha quando pertinentes. Preserve fontes brutas; fixtures públicas/sintéticas identificadas evitam copiar dados sensíveis.
- Controle relógio, aleatoriedade, caminhos e fronteiras externas quando isso for parte do teste. Uma seed global não controla sozinha todos os estimadores, threads, backends ou serviços.
- Compare conteúdo ou propriedades que realmente detectem o defeito. Shape, dtype e soma podem coincidir entre resultados diferentes. Para arrays/tabelas, confira chaves, valores e alinhamento relevantes; para APIs, status/payload e transições; para CLI, streams, exit codes e efeitos em diretórios temporários.
- Defina tolerâncias numéricas pela precisão e domínio, com casos próximos de zero quando pertinentes. Não copie `rtol=1e-5` para todo cálculo.
- Normalize apenas volatilidade conhecida e irrelevante, como caminho temporário, preservando campos que fazem parte do contrato. Não remova erro, timestamp de negócio ou diferença significativa para obter snapshot verde.
- Aprove a baseline por inspeção; não atualize snapshots indiscriminadamente. Guarde dados de entrada e ambiente suficientes para reexecutar sem segredos.

## Correções de comportamento

Registre o comportamento atual e o desejado, com motivo e critério de aceite aprovado. Acrescente teste do requisito corrigido e demonstre a falha esperada antes de implementar quando viável. Requisitos de segurança ou integridade não devem ficar congelados como comportamento correto.
Toda alteração intencional precisa dessa distinção, seja P0, P1 ou outra prioridade. Não trate P0 como licença para quebrar testes, nem bloqueie correção aprovada de outro nível apenas por não ser P0.

## Verify, recuperar, parar

1. Antes da fatia, identifique base, arquivos e estado staged/unstaged/não rastreado. Registre patch/backup ou use isolamento apropriado sem sobrescrever trabalho prévio. Não faça stash, reset ou checkout geral para obter árvore limpa.
2. Verifique os testes afetados e as dependências da fatia; execute checks integrados obrigatórios no fechamento e quando o risco exigir. Registre os resultados observados, sem esconder falhas preexistentes.
3. Havendo diferença não autorizada, interrompa novas fatias. Se diagnóstico indicar reversão, remova apenas suas edições, preservando alterações anteriores e posteriores de outros autores. Snapshot de arquivo inteiro só é seguro sem edições concorrentes naquele arquivo desde a captura.
4. Não use `git checkout -- <arquivos>` como desfazer universal: ele restaura o índice e pode descartar alterações unstaged que já existiam antes da fatia. Se a aplicação inversa não for segura, preserve evidências/diff e resolva o conflito antes de prosseguir.
5. Confirme a recuperação com checks relevantes. Repetição de falha sem nova evidência exige replanejamento, não tentativas ilimitadas ou alteração do oráculo.

Falha de ambiente, requisito conhecido não atendido e regressão introduzida são estados diferentes; todos devem aparecer no relatório quando limitarem o aceite.
