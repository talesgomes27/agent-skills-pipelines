# Plano de melhoria mensurável

Registro histórico de 2026-10-22, preservado como evidência das decisões daquela execução. O [roadmap de modernização](audits/modernization-2026-10-28/roadmap.md) é o sucessor para o programa MOD; o estado e a autorização vigentes estão no início de [task.md](../task.md). Aprovações deste registro não autorizam novas ações.

Data: 2026-10-22. Origem: recomendações aceitas pelo usuário.

## Objetivo e invariantes

Melhorar a qualidade observável das skills e a confiabilidade da distribuição. Preservar nomes, responsabilidades, recursos relativos, instalações existentes e alterações do usuário. Nenhuma etapa publica artefatos ou executa ações remotas.

## Fatias

1. **Harness comportamental:** casos positivos, ambíguos e negativos por skill; formato de resultados; grader determinístico para roteamento, operações proibidas, artefatos e métricas; testes unitários. O harness não afirma qualidade sem execuções reais.
2. **Modos de aprovação:** introduzir `assistido` e `contínuo` nas pipelines com gates, mantendo parada em mudança material e ação externa não autorizada. A autorização já dada deve ser reutilizada.
3. **CI:** executar testes, doctors e instalação temporária em Linux, Windows e macOS. Não publicar nem modificar perfis.
4. **Descoberta:** comando que verifica localização e manifesto e, opcionalmente, registra resultado de smoke fornecido por cada host. Codex será confirmado pelo catálogo desta sessão; ausência de Claude/Antigravity não vira sucesso.
5. **Versão:** adicionar versão do conjunto ao catálogo e recibos; detectar atualização disponível sem sobrescrever alterações locais.
6. **Biblioteca fria:** validar índice contra manifests, produzir relatório e permitir reconstrução em arquivo escolhido. A operação padrão é somente leitura.

## Verificação e recuperação

- Cada fatia acrescenta testes antes ou junto da implementação.
- `python3 -m unittest discover -s tests -v`, doctors e `git diff --check` fecham a integração.
- Edições ficam em arquivos novos ou patches delimitados. Se uma fatia falhar, interromper as seguintes e preservar o diff para correção; não usar reset ou checkout global.
- As cópias instaladas no Codex só serão atualizadas depois da validação integrada, usando o instalador gerenciado e preservando a `humanizer` padrão escolhida pelo usuário.
