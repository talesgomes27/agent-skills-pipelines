# Triagem por impacto e evidência

Preserve a escala do projeto quando houver. Caso contrário, use P0–P3 como prioridades justificadas pelo cenário, separando severidade do problema, confiança na evidência e ordem de execução.

| Prioridade | Critério contextual | Resposta |
|---|---|---|
| P0 — Crítico | Dano grave imediato ou bloqueio crítico confirmado no contexto de uso, como exposição ativa de credencial privilegiada ou corrupção de dados em operação | Informar e priorizar contenção/correção autorizada; não publicar segredo no relatório |
| P1 — Alto | Risco material de segurança, integridade ou função essencial, com impacto e alcance demonstráveis | Planejar proteção e correção prioritária |
| P2 — Médio | Defeito ou dificuldade de manutenção relevante, com consequência localizada e evidência | Planejar conforme benefício, dependências e custo |
| P3 — Baixo | Ajuste de baixo impacto ou convenção local sem comprometimento funcional importante | Opcional se houver justificativa e autorização de escopo |

Falha de build pode ser P0/P1 ou limitação local conforme alcance e ambiente. Leakage, citação sem fonte ou seed ausente exigem análise do uso e consequência; não atribua prioridade máxima só pelo rótulo. Falta de `freeze`, pt-BR, DPI específico, gerenciador uv ou seção CRISP não é defeito sem requisito correspondente.
Centralidade do grafo, complexidade ciclomática, cobertura e alertas de scanner orientam investigação, não definem automaticamente severidade ou obrigatoriedade de alterar código.

## Achado verificável

Use a tabela do chamador:

| ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico |
|---|---|---|---|---|---|

Para cada achado, inclua junto à linha ou em nota identificada: cenário, evidência/reprodução, impacto, confiança e verificação proposta. Use localização real e excerto curto. Diferencie confirmado, hipótese e não verificável com os acessos atuais.
Não reproduza tokens, senhas, dados pessoais ou payloads privados para sustentar o achado; use referências e excertos minimizados.

## Plano de resposta

Ordene por dano, dependências e capacidade de validação. Uma preparação pequena pode ser necessária antes de corrigir o achado mais grave. Aprovação do relatório reconhece achados e prioridades; não aprova automaticamente toda sugestão, migração, rotação de segredo ou mudança funcional.
Mantenha estado por ID: aberto, planejado, resolvido, não confirmado ou aceito com ressalva. Registre quem aceitou a ressalva a partir de evidência real; não invente aceite para encerrar o ciclo.
