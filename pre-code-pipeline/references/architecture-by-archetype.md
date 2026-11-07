# Arquitetura por arquétipo

Leia só a parte do arquétipo registrado e, em projeto híbrido, a do domínio secundário nas partes que ele usa.

## A: análise e modelos

- Separe preparação, análise e publicação, e registre de onde vem cada dado e onde cada resultado é gerado.
- Em estudo acadêmico, siga a organização do formato pedido.
- Em Quarto, siga a [checklist](quarto-quality-checklist.md) e defina no Gate 4 idioma, formato, política de execução e pré-requisitos de renderização; o `.qmd` pode ter só cabeçalhos e placeholders.

## B: aplicações

- Limites e persistência proporcionais ao domínio, com DDD, C4 ou OpenAPI só quando a complexidade pede.
- Mudança de esquema num banco que já tem dados de produção entra na arquitetura como plano de migração, com backup, etapas compatíveis e volta; a `release-and-ops-pipeline` tem a referência de migrações.

## C: automações

- Entradas, saídas, erros, exit codes e idempotência.
- Num job agendado, também horário e fuso, onde o estado fica entre execuções, nova tentativa e quem recebe o alerta de falha.
- Coleta em sites ou APIs de terceiros declara a fonte, os termos de uso e o robots.txt que valem, o ritmo das requisições e o que fazer diante de login ou CAPTCHA.
