---
name: writing-pipeline
description: "Redige, edita e revisa documentos técnicos com preservação de fatos e fontes. Use para PRDs, ADRs, relatórios, READMEs, manuais e revisões editoriais em tabela."
---

# Escrita e revisão técnica

Entregue texto adequado ao leitor, ao documento e às evidências disponíveis. Preserve fatos, números, qualificadores, unidades, comandos, identificadores e significado durante edições; mudanças de conteúdo exigem fundamento explícito.

## Entrada e seleção

- Identifique documento-alvo, público, idioma, formato, objetivo e modo a partir do pedido, das instruções locais e do texto existente. Leia o alvo antes de editar. Respeite a voz do autor e as convenções do projeto.
- Use `docs/00_archetype.md` se existir ou se for encaminhado por outra pipeline; não crie esse arquivo como efeito da revisão de um texto. Para escrita avulsa, o tipo de documento pode bastar. Pergunte apenas se uma lacuna impedir preservar o significado ou atender ao pedido.
- **Modo 1 — redação/edição:** crie ou altere o alvo quando isso estiver autorizado pelo pedido ou pela tarefa encaminhada.
- **Modo 2 — revisão não destrutiva:** entregue achados e sugestões sem modificar o alvo. Preserve o formato de achados exigido pelo chamador; consulte o [protocolo de revisão](references/review-protocol.md).
- Consulte o [guia por documento](references/document-types.md) apenas para a modalidade necessária. Para citações, bibliografia ou afirmações quantitativas, consulte [fontes e evidências](references/citations-and-evidence.md).

## Fluxo

1. Delimite o trecho e o resultado solicitado. Reaproveite informações já disponíveis; não leia todas as referências nem toda a base de código para revisar um parágrafo.
2. Separe alegações factuais, hipóteses, requisitos planejados e decisões. Confira as afirmações materiais em código, configurações, saídas ou fontes fornecidas. Para documentação factual, confronte o comportamento observado; para PRDs e planos, preserve o caráter futuro dos critérios. Divergência entre especificação e código é um achado, não autorização para mudar o contrato.
3. Organize a informação conforme a tarefa do leitor. Explique o resultado ou ação principal cedo e mantenha uma ideia central por parágrafo. Use listas e tabelas quando melhorarem comparação ou execução.
4. Redija ou proponha a edição mantendo a evidência. Corte repetição e linguagem promocional sem retirar limitações, pré-requisitos ou distinções técnicas. Não imponha cotas de frases curtas, desvio padrão de palavras, sinônimos artificiais ou variação por aparência.
5. Confira termos, números, referências, exemplos e sintaxe no escopo alterado. Use ferramentas configuradas no projeto para checks repetíveis; não declare precisão factual a partir de lint, link HTTP válido ou presença de chave bibliográfica.
6. Entregue o texto/arquivo no Modo 1 ou os achados no Modo 2. Resuma mudanças materiais, verificações e pendências quando útil; para uma pequena edição sem limitações, evite relatório adicional.

## Preservação de conteúdo

- Não transforme adjetivos vagos em benchmarks, SLAs, percentuais ou causalidade inventados. Sem evidência, remova a alegação vazia, peça o dado indispensável ou registre a lacuna fora do texto final. Não substitua um valor desconhecido por um número plausível.
- Preserve jargão correto, citações literais e exemplos de código. Uma blacklist não justifica trocar nomes de domínio ou termos como robustez estatística e escalabilidade quando têm significado preciso.
- Adeque registro e comprimento à informação. Clareza tem precedência sobre um molde de voz, proibição genérica de prosa ou meta de detecção de IA. Não prometa autoria humana ou indetectabilidade.
- Se faltar evidência material, não apresente a afirmação como verificada. No Modo 1, entregue rascunho/trecho seguro e destaque a pendência; no Modo 2, registre o achado. Suspenda apenas o trecho ou decisão dependente, quando possível.
- Não execute comandos com efeitos externos para validar exemplos sem autorização. Versões, flags e símbolos podem ser conferidos no código, ajuda da CLI e documentação oficial; execução real depende do escopo permitido. Redija separadamente o que foi observado e o que foi apenas inspecionado.

## Fontes, formato e especialistas

Bibliografia e estilo de citação pertencem ao projeto/documento. Resolva chaves nos arquivos e metadados configurados, usando o parser/motor adequado quando disponível. Um catálogo editorial da skill pode sugerir leituras; não autoriza citações nem substitui a bibliografia efetiva.
Links devem apontar à fonte que sustenta a afirmação. Metadados confirmam identidade bibliográfica, não sustentação de conteúdo. Cite somente o que foi consultado ou marque a verificação pendente, sem fingir leitura do texto integral.
Para Quarto, preserve formato, bibliografia e referências cruzadas existentes; use `quarto-expert` quando a tarefa exigir conhecimento específico de configuração/renderização. Criar `.qmd` não autoriza reexecutar análises custosas ou publicar.
Use `humanizer` apenas quando disponível e útil à revisão de estilo solicitada, preservando estas restrições de significado e evidência. Não carregue uma segunda cadeia editorial para cada docstring. Conectores/MCP existentes podem acessar fontes privadas autorizadas; não instale servidor ou conecte conta para uma edição local simples.
Se um relatório Graphify for pertinente ao documento, confira escopo, cobertura e atualidade antes de citar. Não acrescente uma seção arquitetural apenas porque o arquivo existe; métrica do grafo não prova qualidade do projeto.

## Integração e conclusão

A pipeline chamadora mantém seus gates, estado e critérios de aceite. Esta skill devolve artefatos e pendências, sem marcar aprovação do usuário, iniciar outro gate ou fazer commit/publicação. Não crie um plano paralelo.
No Modo 1, atualize apenas os arquivos autorizados e confira o diff. No Modo 2, preserve o alvo e indique localização e evidência dos achados. Nunca apresente rascunho com pendência factual impeditiva como pronto para publicação; o chamador decide o avanço com esse estado explícito.
