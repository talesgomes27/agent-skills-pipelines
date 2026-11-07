# Retreino agendado

Retreino é um job e segue o contrato da skill. Ele também segue as regras de método da pipeline para o modelo: split temporal quando o problema pede, ajuste só no treino e comparação com o baseline. Esta referência acrescenta o que muda quando o treino se repete sozinho.

## Antes de agendar

- Defina de onde chegam os dados de cada rodada, como eles são validados antes do treino (esquema, faixa de valores, volume) e o que o job faz se o período novo não chegou.
- Defina o que é retreinado: só os parâmetros do mesmo modelo, ou também a escolha do modelo e dos hiperparâmetros. Trocar de modelo sozinho é decisão do usuário e fica registrada no plano.

## Versão e guarda

- Cada rodada grava o modelo com versão: data de corte dos dados, commit do código, parâmetros e métricas. Use o lugar mais simples que sobrevive ao runner: um asset de release ou um bucket com um manifesto em JSON. Um registry como o MLflow compensa quando há vários modelos ou outro sistema que os consome. Artefato grande não vai para o Git.
- Guarde as previsões publicadas com a versão do modelo que as gerou.

## Promoção

- O modelo novo substitui o atual só se passar no critério do plano, medido no mesmo período de validação e contra o baseline. Um exemplo de critério: erro agregado não pior que o atual e um limite para a piora nos grupos que importam, como as maiores lojas. Com séries curtas, um critério por loja oscila demais.
- Sem critério aprovado, o job grava o candidato e avisa, sem promover.
- Mantenha a versão anterior pronta e diga como voltar a ela.

## Acompanhamento

- Quando os valores reais chegam, calcule o erro das previsões já publicadas, por versão do modelo, e alerte quando ele passa do limite do plano.
- Confira a deriva das entradas (distribuição, volume, categorias novas) antes de confiar numa rodada.
- Relatório recorrente, em Quarto ou dashboard, é gerado a partir da versão promovida e mostra a data de corte dos dados. O job renderiza de novo com os dados da rodada, sem reaproveitar um `_freeze/` antigo, e publica no destino do relatório. Se o relatório é público e os dados não, renderize onde os dados estão e publique só o resultado saneado.
