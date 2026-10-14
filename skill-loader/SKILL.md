---
name: skill-loader
description: "Carrega dinamicamente sob demanda qualquer skill armazenada na biblioteca fria."
---

# Skill Loader (On-Demand Cold Storage)

Quando o usuário solicitar explicitamente uma skill arquivada (ex: "use a skill X"), acesse o caminho da biblioteca fria (`/home/tales/.gemini/config/skills-library`), leia o arquivo principal de instruções dessa skill (`/home/tales/.gemini/config/skills-library/<nome-da-skill>/SKILL.md`) e aplique suas diretrizes nesta tarefa.

## Procedimento de Carregamento Sob Demanda

1. **Localizar a skill na biblioteca fria**:
   - Caminho padrão: `/home/tales/.gemini/config/skills-library/<nome-da-skill>/SKILL.md`
   - Para buscas por palavra-chave, categoria ou tags, consulte o índice estruturado local em `/home/tales/.gemini/config/skills-library/skills_index.json`.
   - Caso o nome exato não seja conhecido, filtre os diretórios em `/home/tales/.gemini/config/skills-library/`.
2. **Ler as instruções**:
   - Utilize `view_file` em `/home/tales/.gemini/config/skills-library/<nome-da-skill>/SKILL.md` (e em eventuais arquivos auxiliares referenciados dentro da pasta da skill).
3. **Aplicar diretrizes**:
   - Siga integralmente o fluxo, checklists e restrições definidos na skill carregada durante a execução da tarefa atual.
