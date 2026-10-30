# Meta-Skills 2.0.0 — candidata de CI

Base aprovada: 33b773cf099c6be3183526b31b758d783260cbd1. Branch autorizada: codex/meta-skills-2-candidate. Catálogo e README recebem 2.0.0 para testes, sem merge/tag/release/publicação. DEL não integra esta candidata.

- API.md: quatro fronteiras públicas, migração e diferenças schema/CLI.
- COMPATIBILITY.md e RELEASE-NOTES.md: compatibilidade e notas propostas.
- contracts/grade-output.schema.json: proposta de contrato para saída processed, verificada contra resultados preservados; não altera o runtime.
- evaluations-v2/: proposta prospectiva, separada e não executada.
- schema-matrix.json: 12 observações históricas da preparação local; as fronteiras serão novamente conferidas antes do commit.
- SECURITY.md e security.json: consultas atuais e limitações de segurança.
- CI-PREPARATION.md: escopo, arquivos, ajustes e gates autorizados.

Artefatos binários, manifests, logs e relatório da preparação anterior permanecem locais e identificados por seus hashes; não são adicionados automaticamente ao Git. O parecer posterior vinculará a CI ao commit exato. Aprovação estrutural não aprova avaliações comportamentais nem publicação.
