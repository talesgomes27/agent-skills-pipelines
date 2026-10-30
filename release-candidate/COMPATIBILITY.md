# Matriz da candidata

| Contrato / ambiente | Estado |
|---|---|
| Nomes, bundles, flags e recibo v1 | Preservados; testes locais de instalação/atualização |
| Catálogo/schema versão 1 | Retido; release 2.0.0 somente na branch candidata |
| JSON summary numérico antigo | Incompatível para desconhecidos; migrar consumidores a null/observações |
| Contagem tokens:1 | Schema e CLI aceitam |
| Contagem tokens:1.0 | Schema aceita; CLI rejeita; perfil operacional explícito |
| Metadados extras em trace | Rejeitados; usar sidecar |
| Schema catálogo isolado | Não verifica pertencimento dinâmico de bundles; CLI obrigatório |
| Linux / Python 3.14.4 | Verificação local; nova execução registrada separadamente da preparação anterior |
| Python 3.9 / Windows / macOS | CI remota pendente; não inferir aprovação a partir de YAML |
| Cópia/link em temporário | Ver evidências da preparação e parecer de CI; link acompanha fonte viva |
| Instalação nativa/perfis reais | Não executada |
| Coortes históricas | Preservadas, failed originais; v2 é proposta pré-execução |

Nenhum consumidor externo foi exercitado. Aprovação de publicação exige decisão de API/versão, CI do conteúdo final e avaliação das limitações.
