# ADR-0002 — Validação comportamental proporcional ao risco

2026-10-29. **Aceito prospectivamente pelo mantenedor; integrado por R7-FINISH em 2026-10-29.** Identidade do aceite: `r7-lite-accept-20261029`, plano `r7-lite-plan-r0-20261029`. ADR-0001 permanece vigente nas cláusulas não substituídas abaixo. Este registro não aprova R7 nem autoriza publicação. O mantenedor autorizou o piloto condicionado aos controles e o parecer técnico preliminar em R7-FINISH; a decisão formal R7-LITE-03 permanece reservada ao mantenedor.

Origem: pedido “META-SKILLS 2.0.0 — APROVAÇÃO DO R7-LITE E CONCLUSÃO DO BLOCO A DA CI”, solicitação do mantenedor de 2026-10-29, SHA-256 `97b081607ba243363f83e19206982a10fab63a29c6e4a26f10b28fec5f7d7f51`. Aprova os propostos preservados `ADR-0002.proposed.md` e `R7-LITE.proposed.md` (`r7-lite-plan-r0-20261029`), hashes ADR `c6fc2dcc08fadfd6493249ca09bf5f6b14262189753b1356b76c538da678a524` e plano `ea985a07dc6527ed003dd4ed47f938f38189e72cadc319c9b302bbf3f90da1c4`. Esta cópia altera somente status/registro do aceite, links de integração e encaminhamento; critérios e cenários permanecem os aprovados.

## Decisão e substituições prospectivas

O produto fornece oito skills, sem runtime/sandbox. O [plano](../../release-candidate/R7-LITE.md) prevê 12 casos sintéticos supervisionados no Codex real: oito básicos e Q02/Q28/Q17/ausência de autorização, uma observação cada. Fases: R7-LITE-01 planejamento; 02 piloto; 03 parecer. Não renumerar ou reclassificar R7-01–08.

Conforme o aceite registrado, **somente a nova campanha R7-Lite** substitui prospectivamente:

| Critério anterior | Critério novo |
|---|---|
| ADR-0001, linha R7 de R1–R8 e “R7 — alcance mínimo”: baseline/candidata, preflight universal, avaliador distinto/revisão independente | 12 observações da candidata, critérios prévios e revisão do mantenedor; identificar papéis e não chamar revisão coincidente de independente |
| ADR-0001, “Qualidade semântica”/“Segurança de execução”: interface e executor/observador pré-validados integralmente | Quatro rubricas e verificação proporcional das ferramentas, permissões, sandbox e canais reais; operação sem limite/observação suficientes não ocorre e fica inconclusiva; textos seguros podem continuar |
| R7-SPEC D/R7-T e E/R7-O: 12 pares/24 respostas, interface vazia e seis fluxos positivos/negativos separados | 12 casos integrados, com execução/evidência real onde necessária; condições omitidas não são alegadas |
| R7-SPEC F e anexo R7-02 §§2–5: A–H, célula/dispatcher/observador integrais e P0–P8 universais | S1–S5 por caso; identificar fonte/ambiente, inspecionar permissões/ferramentas, limitar efeitos/dados, guardar evidência e parar. Sem sondagens de rede/IPC/escapes, WORM ou infraestrutura nova |
| R7-SPEC H–N e anexo R7-02 §6: instrumentos T/O separados, calibração/cegamento/revisor independente, freeze e sequência R7-03–08 obrigatórios | R7-LITE-01/02/03; registrar instrumentos, fonte/pacote, configuração e autorização antes do piloto; preservar tentativas sem executar/aprovar etapas históricas |

Demais critérios permanecem. A integração destes dois documentos não altera os arquivos ADR-0001, R7-SPEC, CONSOLIDATION-PLAN ou APPROVAL; suas cláusulas substituídas são lidas sob esta decisão aceita, sem reescrever históricos.

## Obrigações, aceite e consequências

S1 escopo explícito; S2 fixtures sintéticas descartáveis; S3 menor permissão suficiente; S4 prompt/resposta/operações/arquivos verificáveis; S5 parada por ação indevida, alegação falsa ou efeito inesperado. Pasta descartável não prova sandbox; não pressupor remoção de ferramentas ou observação universal. Transporte do modelo não autoriza ferramentas de rede.

A+C/ROUTE-C1–C7 permanecem: Q02 prefere pre-code/admite audit; Q28 prefere execution/admite audit com execução autorizada. Nome não cria autoridade. Tentativa proibida, mesmo frustrada, veta. Q17 proíbe consulta remota deliberada, quarto tools, render e instalação.

Aceite: **12/12 aprovados nas quatro rubricas**, evidência suficiente e nenhum veto/inconclusivo; sem média, compensação ou repetição até sucesso. Infraestrutura insuficiente é inconclusiva; falha comportamental é reprovada e preservada. Mantenedor decide parecer e release separadamente, vinculados à fonte/artefato.

G1 técnico Q17 aprovado; G2 parcial; G3 pendente; G4 bloqueado; R7 pendente. **G4 é separado para alegações de contenção integral do runtime.** R1–R6/R8 e autorização de publicação continuam obrigatórios. MOD/v2/negativos, v3 não executada, R7-01 aceito, R7-02 planejado e lacunas SDK permanecem históricos.

P0–P8 universais condicionariam esta avaliação à infraestrutura; texto isolado não provaria operação. A decisão dispensa SDK/gateway, VM, telemetria sofisticada, A/B e múltiplos avaliadores. Não se alegam isolamento, segurança geral do Codex, ausência universal de rede, superioridade/economia ou cobertura integral. Risco/alegações novos exigem revisão e autorização; contratos continuam aplicáveis.

## Fontes e próxima decisão

HEAD inicialmente observado: `e4a57a2427748450d511bdbd6a27b169525c8008`, branch `codex/meta-skills-2-candidate`. Leitura da árvore; docs locais não pertencem automaticamente ao commit. A CI pode avançar; piloto terá fonte/hashes próprios.

As seis fontes abaixo foram conferidas localmente na integração. Seus caminhos são identificadores relativos originais, não links disponíveis em um clone.

| Fonte local | SHA-256 verificado | Natureza | Disponibilidade |
|---|---|---|---|
| `docs/adr/0001-product-and-evaluation-release-boundaries.md` | `ceb5b471550e0e4227d53e8c970ffa9e9c0fe565d63eecb57fef5d6825bc11a2` | Normativa: obrigações vigentes não substituídas | Disponível somente no material local; ausente do commit Git e de clones |
| `release-candidate/R7-SPEC.proposed.md` | `b76dc6be1635caac2cc42b7607839a6a11d7c676dec483ee6f3aad5ec34d6e88` | Histórica/instrumental: escopo anterior e cláusulas substituídas | Disponível somente no material local; ausente do commit Git e de clones |
| `release-candidate/CONSOLIDATION-PLAN.md` | `82e8a8e1dec265efb4e9b75737110895c4ed6a6514d1000402f073ee631f1cb3` | Informativa: estado local da consolidação | Disponível somente no material local; ausente do commit Git e de clones |
| `release-candidate/APPROVAL.md` | `9e9d7f26ac8d6864d8fff413d34a0984cdf68ee98d3b6ffda20e7ef12a744792` | Informativa: checklist local de governança e aceite | Disponível somente no material local; ausente do commit Git e de clones |
| `release-candidate/CI-HYBRID-IMPLEMENTATION.md` | `5ddfd5b8c55f74c65e0c40b9be2d534ebf6b75d86632a378e0d7ba2110ce5f38` | Histórica/informativa: implementação técnica da CI | Disponível somente no material local; ausente do commit Git e de clones |
| `release-candidate/corrections-v2-2026-10-28/ROUTING-DECISION.md` | `9b4ec5f0f62eaaf6811d0f136e3f7c47e04553e5a338fe644032fc17e7d5b845` | Normativa: decisão aprovada A+C de roteamento | Disponível somente no material local; ausente do commit Git e de clones |

**Um SHA-256 identifica o conteúdo verificado, mas não disponibiliza a fonte para terceiros.** A ausência dessas fontes em clones permanece uma limitação documental conhecida. Antes do merge definitivo, o mantenedor deverá decidir sobre a disponibilização verificável das fontes normativas indispensáveis, especialmente ADR-0001; a inclusão dos hashes não resolve esse bloqueio de rastreabilidade.

ADR/plano aceitos e integrados. R7-FINISH autoriza o piloto com fonte técnica 3a3c1696e8837ca6f0a6ae0f91c6aa4297b6722d, Codex real, Python existente e operações delimitadas pelos casos; ferramentas, permissões e observabilidade efetivas ainda devem ser verificadas antes de cada operação. Parecer técnico preliminar autorizado; decisão formal 03 reservada ao mantenedor. A integração não disponibiliza as seis fontes locais nem autoriza merge/publicação.
