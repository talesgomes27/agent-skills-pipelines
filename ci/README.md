# CI híbrida da candidata 2.0.0

A candidata não está publicada. Este conjunto versiona a receita e os controles de CI;
a execução remota e a aprovação da release continuam pendentes. O produto distribui
oito skills e utilitários, sem DEL/Subagent-Optimation ou runtime próprio de agentes.

## Fonte, pacote e transporte

- [Seleção](payload.json): 82 fontes fixadas por caminho, tamanho e SHA-256; inclui Q17.
- [Receita](build_payload.py): stdlib, USTAR ordenado, gzip determinístico; acrescenta
  [README fixo](PAYLOAD-README.md) e manifesto, total de 84 arquivos. O CLI exige que
  os 82 arquivos e os três inputs da receita coincidam com blobs do HEAD real.
- [Verificador](verify_payload.py): independente da receita e compatível com Python
  3.9; confere digests externos, commit/run/tentativa, composição e metadados antes de
  extrair para destino novo. Não aceita o manifesto CONS-03 como novo formato híbrido.
- O produtor faz duas montagens e compara os três arquivos: tar, manifesto e delivery.
  Os sete consumidores recebem o mesmo artifact-id do produtor, com digests e identidade
  da mesma execução/tentativa. Nenhum consumidor reconstrói ou escolhe um artifact latest.
- O pacote novo terá identidade própria. O SHA histórico CONS-03 não deve ser exigido
  de um tar cujo manifesto contém outro commit/gerador; as 82 fontes continuam fixadas.

A política preservada escreve as fontes do tar como **0664** e os dois derivados como
**0644**, independentemente da umask/modos de checkout Git. O grupo pode escrever em
fontes extraídas quando tiver acesso. Isso não equivale a imutabilidade, ACL universal
ou segurança de instalação; qualquer mudança de política exige nova identidade e
validação. Em Windows, chmod não certifica semântica POSIX de permissões.

## Oito jobs e dependências

O [workflow](../.github/workflows/ci.yml) define um produtor Ubuntu 24.04/Python 3.14.4,
seis consumidores Ubuntu/Windows/macOS × Python 3.9/3.14 e um consumidor Linux/link.
Os consumidores dependem do produtor. As permissões permanecem contents:read e as
ações são fixadas por SHA; não há etapa de merge, tag, Release ou publicação de pacote.
O upload de artifact é transporte de CI sujeito à autorização para a execução remota,
com retenção de 14 dias; não concede aprovação de distribuição pública.

O produto conserva [Python 3.9+/PyYAML 6.0.3](../distribution/requirements.txt).
O [lock formal](requirements-formal.lock) é exclusivo do produtor Linux/cp314:
jsonschema 4.26.0 e suas quatro dependências, sem impor Python >=3.10 aos consumidores.
O pip fornecido pelo setup/venv deve ter sua versão registrada; não há upgrade automático.
Sua preparação no runner é distinta do zipimport pip 26.2.2 usado na validação local.

[formal_schemas.py](formal_schemas.py) verifica os dois schemas públicos por padrão:
17 controles internos; --proposed-output acrescenta autovalidação explicitamente
rotulada como proposta, sem homologação pública. tokens:1.0 permanece válido no schema
e rejeitado pelo perfil operacional da CLI; validação declarativa não substitui a CLI.
Instrumentos v3 e campanhas comportamentais não fazem parte desse helper.

[offline.py](offline.py) aplica libseccomp a comandos confiáveis Linux x86_64, sem
fallback sem filtro. As 21 regras configuradas não receberam certificação integral:
evidências locais de FDs/IO/Unix/socketpair/recvfrom têm alcance restrito e baselines
IPv4/IPv6 foram inconclusivas. Não é sandbox de agente, proteção geral do filesystem
ou aprovação de G4. Disponibilidade de libseccomp e comportamento no runner precisam
ser conferidos; não instalar infraestrutura global como correção silenciosa.

[check_installation.py](check_installation.py) usa a árvore extraída validada, instala
as oito skills incluindo humanizer, verifica copy/link, upgrade do snapshot local
33b773c/1.0.1, idempotência e proteção de alterações. --recovery exercita falhas
controladas de recibo e retomada por pacote, sem transação do lote ou queda de energia.
Links acompanham a fonte viva. Não utilizar perfis reais como destino de testes.

A descoberta selecionada passa a conter **87 testes**: 62 oficiais anteriores mais
25 de [test_payload.py](../tests/test_payload.py). Essa contagem não inclui o teste
local experimental test_v3_isolation.py, que permanece fora da seleção. Os consumidores
executarão a descoberta completa sem skips; o produtor executará os 25 de payload.
Doctor/casos estruturais e integrações de fonte/artefato complementam os testes.

## Evidências locais reutilizadas e pendências

As identidades dos executáveis/testes foram confrontadas com os lotes locais:

- CONS-03/06/06.A: pacote histórico e validação de fonte/contratos, nos próprios escopos.
- Segundo lote dos 25 testes de payload: 25/25, sem falhas/erros/skips.
- CI-INTEGRATION-01: nove controles de instalação/upgrade/recuperação, copy e link.
- CI-FORMAL-03: instalação offline autenticada, origens/RECORDs e 12 cenários, sem retries;
  17 controles no fluxo padrão e 18 na seleção proposta explícita.
- CI-OFFLINE-01 inconclusivo, 02/03 com evidências restritas; não aprovação integral.
  CI-FORMAL-01/02 continuam inconclusivos; as correções dos observadores temporários
  não integram o produto nem este conjunto executável de CI.

As evidências detalhadas permanecem locais e preservadas; este commit não as arquiva
nem as inclui como inputs do produtor. Testes locais não validam o pipeline completo,
o transporte Actions ou os pacotes ainda não gerados a partir do próximo commit real.
A compatibilidade dos runners/Node/ações fixadas, a toolchain 3.14.4, o pip efetivo,
libseccomp, os modos extraídos e os oito jobs precisam de verificação no Bloco B.

G1 permanece aprovado somente técnico Q17; G2 parcial, G3 pendente e G4 bloqueado.
R1–R8 não são promovidos por este commit. R7 e a autorização expressa do mantenedor
continuam necessários para publicação; propostas documentais paralelas não alteram
a governança vigente sem aceite humano. Sem alegações de isolamento integral,
segurança universal, aprovação comportamental ou economia medida de tokens/franquia.

## Próxima execução autorizável

Depois de autorizado o Bloco B, usar checkout Git limpo do SHA real, diretórios novos
e inputs commitados para gerar/verificar o pacote e testar o artefato real. O verificador
exige --commit, --run-id, --attempt e os digests de tar/manifest/delivery. Conferir os
oito jobs individualmente após um push normal especificamente autorizado; cancelado
ou não executado não significa aprovado. Nenhum comando de build/push foi executado
como consequência da revisão e do commit local do Bloco A.
