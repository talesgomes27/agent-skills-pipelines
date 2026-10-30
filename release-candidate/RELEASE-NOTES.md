# Notas propostas — 2.0.0 candidata

Não publicada. Versão 2.0.0 autorizada exclusivamente para a branch candidata e testes de CI; não representa tag ou release aprovada.

## Migração
- Consumidores do harness devem aceitar totais null, consultar metric_observations e exigir coverage.complete/evaluation conforme seu gate. Exit 0 não significa avaliação aprovada.
- Traces devem respeitar o perfil estrito: sem campos extras, contagens inteiras não negativas (serializar 1, não 1.0), sem bool/null em métricas. Proveniência adicional vai em sidecar.
- PyYAML deve existir no ambiente de uso do loader/CLI; o instalador não baixa dependências.
- Atualizações gerenciadas exigem --update. Edições locais continuam protegidas; falha tardia pode deixar os pacotes anteriores concluídos. Não apagar recibo para forçar sucesso.

## Entregue
Validação segura de manifests; cobertura e métricas honestas; governança temporal e links; esforço proporcional e handoff; avaliações rastreáveis; actions fixadas e recuperação por pacote testada. Oito skills e seis bundles preservados.

## Limitações
Grades históricos MOD-007/008 continuam failed; propostas v2 não substituem resultados antigos. Nenhuma economia de franquia demonstrada, descoberta nativa ou publicação nesta etapa. A CI remota será registrada por commit e run no parecer posterior. Planos DEL excluídos. A versão anterior usada no teste é um snapshot local declarado 1.0.1, não uma release remota cuja existência tenha sido consultada.
