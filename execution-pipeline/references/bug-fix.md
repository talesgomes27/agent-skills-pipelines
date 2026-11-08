# Correção de bug

Leia antes de editar o código numa correção de erro, bug ou regressão. Quando a correção é tarefa pequena e quando é incidente está no `SKILL.md`.

1. Reproduza antes de mudar, com o comando e a saída que mostram o erro. Se não conseguir, porque o comando foi negado ou falta o ambiente, não edite: diga o que falta e espere.
2. Escreva o teste que falha pelo motivo certo, com a forma real da entrada que quebrou (cabeçalho, payload, formato), sem dados pessoais; sem teste possível, caracterize o comportamento.
3. Corrija a causa, não o sintoma, com o menor diff, e procure os outros pontos que chamam o código mudado.
4. Rode o teste novo e os checks afetados.
5. Registre na resposta, ou onde o projeto já registra estado, a causa, a correção e o que ficou sem verificar. Refatoração vista no caminho vira proposta, não entra no conserto.
