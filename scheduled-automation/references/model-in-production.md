# Modelo em produção

Vale para pontuar um modelo de forma recorrente (uma lista semanal, um score diário), servi-lo por API e retreiná-lo. O job segue o contrato da skill. O modelo segue as regras de método da pipeline: split temporal quando o problema pede, ajuste só no treino e comparação com o baseline. Esta referência acrescenta o que muda quando o modelo sai do notebook e passa a rodar sozinho.

## Do notebook ao pipeline

- Extraia do notebook o preparo dos dados, o treino e a pontuação para funções ou scripts versionados, com as dependências fixadas.
- Reproduza o treino pelo pipeline e compare as previsões com as do notebook numa amostra fixa. Diferença acima da tolerância combinada no plano bloqueia a produção.
- O mesmo código calcula as features no treino e na pontuação, escrito como módulo que o lote e uma futura API possam importar. Uma segunda implementação, num SQL ou noutro serviço, é a origem mais comum de diferença entre o que foi validado e o que roda.
- Na pontuação, use só a informação disponível naquele instante, como no treino.

## Artefato

- Grave o modelo no formato que a biblioteca recomenda e registre as versões da biblioteca e do Python; carregar com outra versão pode falhar ou mudar resultados.
- Pickle e joblib executam código ao carregar: só carregue artefato que o próprio projeto gerou e guardou.
- Cada versão registra data de corte dos dados, commit do código, parâmetros e métricas. Use o lugar mais simples que sobrevive ao runner, como um asset de release ou um bucket com um manifesto em JSON. Um registry como o MLflow compensa quando há vários modelos ou outro sistema que os consome. Artefato grande não vai para o Git.
- Guarde as previsões publicadas com a versão do modelo que as gerou.

## Lote ou API

- Comece pela pontuação em lote quando quem usa precisa de uma lista periódica: ela é mais simples de testar, refazer e auditar.
- Uma API vale quando a decisão precisa do score na hora, como num atendimento ou num checkout. Ela segue a referência B da `execution-pipeline`, com contrato de entrada, latência combinada e o mesmo código de features.

## Limiar e entrega

- A data de referência e o horizonte da previsão (por exemplo, quem cancela nos próximos 90 dias) são os mesmos do treino.
- Quantos nomes entram na lista, ou qual score dispara uma ação, é decisão de quem usa a lista, pela capacidade da equipe e pelo custo de errar. O plano registra o critério.
- Meça a lista pela taxa de acerto entre os primeiros nomes, comparada com um baseline simples. Quando der, guarde um grupo que não é contatado, para saber se a ação muda o resultado.
- Combine com quem usa a lista se quem já foi contatado sai das listas seguintes.
- A entrega da lista segue a skill `personal-data`: só os campos necessários, canal restrito e destinatário definido.

## Retreino

- Defina de onde chegam os dados de cada rodada, como eles são validados antes do treino (esquema, faixa de valores, volume) e o que o job faz se o período novo não chegou.
- Defina o que é retreinado: só os parâmetros do mesmo modelo, ou também a escolha do modelo e dos hiperparâmetros. Trocar de modelo sozinho é decisão do usuário e fica registrada no plano.
- O modelo novo substitui o atual só se passar no critério do plano, medido com o mesmo protocolo de validação do plano, como as mesmas origens numa série temporal, e contra o baseline. Um exemplo de critério: erro agregado não pior que o atual e um limite para a piora nos grupos que importam, como as maiores lojas. Com séries curtas, um critério por loja oscila demais.
- Sem critério aprovado, o job grava o candidato e avisa, sem promover.
- Mantenha a versão anterior pronta e diga como voltar a ela.

## Acompanhamento

- Quando os valores reais chegam, calcule o erro das previsões já publicadas, por versão do modelo, e alerte quando ele passa do limite do plano. Alguns rótulos demoram: um churn só se confirma meses depois, e o acompanhamento espera por isso.
- Num job só de pontuação, acompanhe também o volume da lista e a distribuição dos scores entre rodadas.
- Confira a deriva das entradas (distribuição, volume, categorias novas) antes de confiar numa rodada.
- Relatório recorrente, em Quarto ou dashboard, é gerado a partir da versão promovida e mostra a data de corte dos dados. O job renderiza de novo com os dados da rodada, sem reaproveitar um `_freeze/` antigo, e publica no destino do relatório. Se o relatório é público e os dados não, renderize onde os dados estão e publique só o resultado saneado.
