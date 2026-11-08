# Spec viva

Uma `docs/spec.md` por projeto é a fonte dos requisitos e continua valendo depois da entrega. Cada requisito tem ID, critério verificável, estado e evidência. O código nunca é gerado a partir da spec: ela diz o que precisa ser verdade, e os testes e as saídas provam.

## Quando o arquivo existe

- Projeto que vai durar além da conversa: a spec é redigida no PC-2 e aprovada no A1, o aceite do fim de PC-5.
- Entrega pontual, tarefa pequena e correção de bug: spec mínima na própria resposta (pergunta, critério e verificação), sem arquivo.
- Projeto que já usa Spec Kit, Kiro ou OpenSpec: a pipeline usa o formato dele, como em [formatos de SDD](sdd-formats.md), e não cria `docs/spec.md`.

## Modelo

```markdown
---
projeto: dashboard-vendas
arquetipo: {principal: aplicacao, secundario: analise}
versao_spec: 1
atualizado_em: 2026-11-20
---

# Spec: dashboard de vendas

## Contexto
Problema, público e decisão que o trabalho apoia, em uma ou duas frases.

## Requisitos
### R-001 Filtro por região
- Enunciado: a pessoa filtra as vendas por uma ou mais regiões.
- Critério: Dado o filtro "Norte", Quando a tela atualiza, Então o total
  mostrado é igual ao da consulta de referência.
- Prioridade: alta
- Estado: aprovado
- Evidência: (preenchida na entrega)

## Fora do escopo
### N-001 Previsão de vendas

## Decisões
### D-001 Streamlit Community Cloud com acesso por convite

## Restrições
- Nenhum campo pessoal na tela (skill personal-data).

## Questões abertas
### Q-001 Quem recebe o alerta de falha da carga diária?
```

O front matter não registra aprovação: o aceite do A1 fica onde o projeto registra estado (`task.md`, issue, PR) ou na conversa, com quem e quando, e o agente nunca o escreve como se fosse do usuário.

Os IDs são `R-` (requisito), `H-` (pergunta ou hipótese, em análise), `N-` (fora do escopo), `D-` (decisão), `Q-` (questão aberta) e `T-` (tarefa do plano), sempre com três dígitos. A forma do requisito muda por arquétipo; veja a [forma da spec](architecture-by-archetype.md#forma-da-spec).

## Ciclo de vida

`proposto` → `aprovado` (no A1) → `implementado` → `verificado` (com evidência ligada) → `obsoleto` (com o motivo).

- Mudar o enunciado ou o critério de um requisito aprovado é mudança de escopo: volta ao A1 e sobe `versao_spec`. A versão anterior fica no histórico do Git.
- Requisito aprovado sem evidência impede chamar a entrega de pronta: no A3, cada requisito aparece com a evidência ou a pendência justificada.

## Rastreio entre spec, plano e testes

- O plano (`docs/plan.md`) lista em cada tarefa `### T-001` uma linha `- Requisitos: R-001, R-002`, os arquivos e a verificação. Os campos podem vir com ou sem o `- ` inicial e com o nome em negrito, um campo longo continua nas linhas indentadas, e blocos de código são ignorados.
- Os testes trazem o ID no nome ou num comentário (`test_r001_...` ou `# R-001`). Em análise, a evidência é a célula rotulada, a saída ou a figura.
- A evidência cita um arquivo que existe, com o teste depois de `::` quando houver: `tests/test_filtros.py::test_r001_total_por_regiao`.

## Verificador

`scripts/spec_check.py` confere a spec sem rede e só com a biblioteca padrão:

```bash
python scripts/spec_check.py --root caminho/do/projeto
```

Ele detecta o formato (`--format auto`, o padrão, ou `native`, `speckit`, `kiro`, `openspec`) e sai com 0 quando está limpo, 1 quando acha problemas e 2 quando não acha spec, não consegue lê-la ou recebe argumento errado. Se houver mais de um formato, ele confere o primeiro, confere também a spec nativa quando ela existe e avisa dos outros. Antes do A3, rode com `--stage a3`; nos formatos de SDD a evidência não é conferida, o script avisa, e o A3 lista a evidência de cada requisito. No formato nativo ele confere:

1. IDs únicos e no padrão, e ao menos um requisito.
2. Todo requisito tem um dos cinco estados do ciclo de vida, e o aprovado, implementado ou verificado tem critério.
3. Todo requisito verificado tem evidência, e o arquivo citado existe; com `--stage a3`, o aprovado ou implementado sem evidência, ou com evidência que cita arquivo inexistente, também é problema. Conta como arquivo o trecho com `/` ou com uma extensão comum (`.py`, `.ipynb`, `.qmd`, `.sql` e outras); URLs são ignoradas, e `::teste` ou `#célula` depois do arquivo são cortados.
4. Com `docs/plan.md`, toda tarefa cita requisitos que existem, e todo requisito aprovado tem tarefa.
5. As questões abertas são listadas no fim, para entrar no resumo do A1 e do A3.

## Documentos antigos

| Hoje | Na spec viva |
|---|---|
| `docs/00_archetype.md` | Front matter da `docs/spec.md`; o arquivo antigo continua aceito |
| `docs/01-data-discovery-and-contracts.md` | `docs/data-contracts.md`, só em análise ou quando há fontes de dados |
| `docs/02-PRD-and-specs.md` | `docs/spec.md` |
| `docs/03-architecture-and-schema.md` | `docs/architecture.md`, opcional, com as decisões `D-xxx` |
| `docs/04-scaffolding-and-conventions.md` | Seção curta no `AGENTS.md` do projeto |
| `docs/05-implementation-plan.md` | `docs/plan.md`, com tarefas ligadas a `R-xxx` |
| `docs/audit-report.md` | Continua; achados citam `R-xxx` quando o código diverge da spec |

Um projeto com os documentos antigos continua funcionando: a pipeline lê e atualiza o que existe e oferece a migração, sem migrar em silêncio.
