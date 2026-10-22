# Smoke tests e recuperação no destino

## Contrato do smoke

Identifique destino, versão/artefato esperado, URL/entrypoint, verificação mínima, timeout e janela de retries antes do teste. Use ações sem escrita por padrão; uma jornada que cria pedido, cobra, envia mensagem ou modifica dados precisa de autorização e conta/dados de teste apropriados.
Registre comando/ferramenta, horário, destino observado, resultado e limitação. Evite registrar tokens/cookies ou dumps privados. Não teste uma URL antiga e atribua o resultado ao novo deployment.

## A: site e publicação documental

Confira uma página representativa e assets pertinentes no output final e no destino remoto. Disponibilidade HTTP deve incluir status esperado, conteúdo/identidade da versão e falhas relevantes de recursos, sem depender só de `index.html` não vazio.
Para HTTP, imprimir `%{http_code}` não cria assert de sucesso. Use cliente/check que retorne falha ou faça comparação explícita do status com o contrato; limite conexão, duração total e retries. Verifique redirecionamento final quando autorizado, sem seguir para host inesperado com credenciais.
Considere propagação de deploy/CDN na janela definida, sem retries indefinidos. Um formato PDF contratado requer sua própria verificação; não inspecione instalação local de browser como prova do site remoto.

## B: serviços e interfaces

Use readiness/jornada mínima pertinente. `/docs` ou `/openapi.json` podem responder enquanto dependências essenciais falham; não os trate como saúde universal. Um 200 também pode ser a página de login ou uma versão anterior.
Compare corpo/contrato e versão quando disponíveis. Latência aceitável vem do requisito/ambiente, não de um limite universal de dois segundos; confirme o que foi medido e por qual duração.
Para UI, valide estado observável da jornada crítica, recursos e erros relevantes; elemento raiz sozinho não comprova funcionamento. Use assertions/locators do runner, não espera fixa ou `networkidle` como condição universal.

## C: pacote ou binário

Teste o artefato final em ambiente temporário e fora do checkout, identificando a versão realmente instalada e removendo dependência de instalação editable. Para Python, use wheel/entrypoint construído, não o código-fonte local por acidente.
Verifique flags que o programa realmente suporta e uma operação mínima segura, incluindo erro relevante quando parte do contrato. `--version` não é obrigatório em toda CLI. Instalação de sdist executa build e deve seguir o mesmo controle de ambiente/credenciais.

## Falha e recuperação

1. Não marque homologação. Distinga falha do produto, propagação, rede, autenticação e erro do próprio teste; registre evidência sem repetir ação externa ambígua.
2. Interrompa promoção ou tráfego adicional quando o plano autorizado assim determinar. Use o procedimento de recuperação previamente definido; autorização específica já concedida pode cobrir o gatilho previsto, sem pedir de novo.
3. Sem autorização aplicável ou com risco de perda de dados, preserve estado e apresente a ação concreta para decisão. `git revert HEAD` pode atingir o commit errado e continua local até publicação; `git checkout <tag>` apenas muda o checkout. Nenhum é rollback remoto universal.
4. Restaure revisão/artefato estável identificado no provedor e trate compatibilidade de dados/schema separadamente. Não mova tags públicas, sobrescreva pacote ou apague recursos para simular recuperação.
5. Reexecute o smoke do destino recuperado. Se não houver recuperação confirmada, informe o estado degradado/parcial, com evidências e próxima ação necessária; não encerre como sucesso.
