---
type: llm
focus: trace
---

PASS se o agente identifica pelo task.md que o próximo passo é o EX-3 (exportar a tabela filtrada em CSV) e confere se a base, o diff ou o destino mudaram antes de reaproveitar checks e aprovações.
FAIL se retoma em outra etapa, recomeça do plano ou reaproveita os checks sem conferir a base.
