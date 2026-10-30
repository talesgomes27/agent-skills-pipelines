# ADR-0003 — Integração técnica com validação comportamental diferida

Data: 2026-10-29. Diretriz prospectiva autorizada pelo mantenedor no Bloco C.
**Preparar commit documental, push, CI e PR está autorizado; o merge depende de confirmação final. Publicação estável não autorizada.**

## Contexto e decisão

A candidata reúne as oito skills, contratos 2.0.0, correção Q17 e CI híbrida. A CI
[40973161241](https://github.com/talesgomes27/agent-skills-pipelines/actions/runs/40973161241)
aprovou oito jobs para `6dd47a492557e3286c52b9a632c70ae996f4256c`.
O novo commit documental exige sua própria CI; essa execução anterior não o aprova.

Adota-se integração técnica com R7 diferido. Aguardar R7 antes de todo merge mantém a
integração dependente de um runtime experimental; dispensar R7 para publicação ocultaria
a ausência de evidência. A alternativa adotada permite revisar e integrar o produto,
preservando o requisito comportamental e o aceite separado da versão estável.

O merge técnico somente é elegível com conteúdo revisado, fontes normativas acessíveis,
CI obrigatória aprovada para a revisão correspondente, riscos registrados, ausência de
publicação automática e confirmação final do mantenedor. Preservar os commits da candidata
via PR; não sobrescrever a main local nem usar privilégios para contornar restrições.

## Relação com ADR-0001 e ADR-0002

[ADR-0001](0001-product-and-evaluation-release-boundaries.md) e
[ADR-0002](0002-risk-proportionate-behavioral-validation.md) permanecem preservados.
Esta decisão esclarece, sem dispensa retroativa:

- ADR-0001, contexto, tabela R1–R8/R7/R8 e consequência de publicação bloqueada:
  os bloqueios à **publicação** permanecem; não constituem veto automático ao merge técnico.
- ADR-0002, “Obrigações, aceite e consequências”: 12/12 e quatro rubricas continuam
  necessários ao parecer R7-LITE-03; CI ou merge não satisfazem esse aceite.
- ADR-0002, “Fontes e próxima decisão”: a pendência de disponibilização normativa é
  resolvida pela inclusão dos dois originais abaixo; a vedação a merge automático permanece.
- Menções anteriores a CI pendente ou restrição da versão à branch candidata são registros
  das etapas anteriores; esta decisão admite integração técnica, mantendo 2.0.0 não publicada.

Não se substituem contratos das skills, A+C, oráculos ou resultados históricos.

## Fontes normativas acessíveis e limites históricos

| Fonte incluída sem alteração de bytes | SHA-256 |
|---|---|
| [ADR-0001](0001-product-and-evaluation-release-boundaries.md) | `ceb5b471550e0e4227d53e8c970ffa9e9c0fe565d63eecb57fef5d6825bc11a2` |
| [Roteamento A+C](../../release-candidate/corrections-v2-2026-10-28/ROUTING-DECISION.md) | `9b4ec5f0f62eaaf6811d0f136e3f7c47e04553e5a338fe644032fc17e7d5b845` |

Os demais caminhos locais da tabela histórica do ADR-0002 e os relatórios de campanha,
CONS-01, SDK e isolamento referenciados pelo ADR-0001 não são incluídos neste commit.
Suas remissões históricas podem não resolver em clones. Os requisitos atuais de merge
estão expressos aqui e no ADR-0002; essas lacunas não são apresentadas como evidência
pública de segurança ou de comportamento. Os brutos temporários do SDK continuam
indisponíveis; não houve reconstrução. Não incorporar acervos experimentais para corrigir links.

## R7, gates e requisitos de publicação

R7 permanece **pendente, não executado e não homologado**, vinculado ao
[plano R7-Lite](../../release-candidate/R7-LITE.md): T01–T12, uma observação por caso,
oito skills demonstradas, quatro rubricas e nenhum veto/inconclusivo essencial.
Nenhuma observação desses casos foi iniciada. Os preflights foram interrompidos por
limitações observadas do sandbox nativo, incluindo falha de preparação com escrita
permitida em arquivo específico; isso não é reprovação funcional das skills.

G1 continua aprovado somente técnico Q17; G2 parcialmente demonstrado; G3 pendente;
G4 bloqueado. Não se certificam contenção integral, segurança operacional geral,
obediência universal, ausência universal de rede ou economia de tokens/franquia.

R1–R6 e R8 continuam sujeitos às evidências da fonte/artefato final e ao aceite do
mantenedor; não são promovidos por este ADR. R7 continua obrigatório para publicação,
com o alcance prospectivo do ADR-0002. Merge, CI, artifact de teste e release são atos distintos.
Tag estável, GitHub Release, registry e divulgação de homologação integral exigem
autorização própria e critérios explícitos; nenhuma dessas ações é disparada por esta decisão.

## Riscos residuais e condições

| Item | Merge técnico | Release estável |
|---|---|---|
| Fontes extraídas 0664, graváveis pelo grupo Unix | Aceitável com risco explícito; não alterar modos nesta fatia | Exige aceite da política e limites; não alegar imutabilidade |
| tokens:1.0 aceito no schema e rejeitado pela CLI | Aceitável com o [perfil documentado](../../release-candidate/API.md); usar contagem 1 | Exige observância da compatibilidade; sem normalização implícita |
| G2 parcial/G4 bloqueado | Aceitável para o pacote, sem certificação de runtime | Bloqueia alegações de contenção não demonstradas |
| R7 sem resultados | Diferido por esta autorização; não bloqueia sozinho o merge técnico | Bloqueante até avaliação e aceite próprios |
| Evidências históricas somente locais | Aceitável com as duas fontes normativas acessíveis e a lacuna declarada | Reavaliar suficiência/retensão no aceite final R2/R8 |

CI não aprovada, fonte normativa ausente, alteração não revisada, publicação automática
ou falta da confirmação final continuam bloqueantes para o merge. O
[workflow](../../.github/workflows/ci.yml) e a [receita](../../ci/README.md) devem ser
conferidos na revisão exata do PR. Qualquer mudança material de conteúdo, base remota,
workflow, alegações ou autorização exige reavaliar os gates afetados antes da ação.
