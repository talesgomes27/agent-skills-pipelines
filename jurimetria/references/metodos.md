# Métodos em jurimetria

Leia quando o trabalho mede tempos, taxas ou resultados de processos, compara unidades ou classifica decisões.

## Tabelas Processuais Unificadas

- A Resolução CNJ 46/2007 cria as tabelas de classes, assuntos, movimentos e documentos, usadas por todos os tribunais. Os processos novos são cadastrados com classe e assunto das tabelas, e os andamentos seguem a tabela de movimentos.
- Os tribunais não mudam classes sem o CNJ, mas podem acrescentar assuntos a partir do último nível e complementos locais de movimentos. Separe os códigos nacionais dos locais.
- O Sistema de Gestão de Tabelas (SGT) tem a consulta pública, o glossário e as versões para baixar. Baixe a versão do período analisado e registre a data dela.

## Tempo de tramitação

1. Escreva no plano, com o usuário: o início (o ajuizamento, ou outro movimento), o evento de fim (pelo código do movimento no SGT, por exemplo baixa definitiva ou julgamento de mérito) e a data de corte da coleta.
2. Para cada processo, o tempo vai do início ao fim; se o fim não aconteceu até o corte, o tempo vai até o corte e o processo é marcado como censurado.
3. Estime a curva de sobrevivência por Kaplan-Meier e relate a mediana com intervalo de confiança, por classe ou por unidade. Use `survival::survfit` em R ou `lifelines.KaplanMeierFitter` em Python.
4. Grupo em que a curva não chega a 50% não tem mediana estimada: relate a proporção encerrada num prazo fixo, como dois anos.
5. Analise por coorte de ano de ajuizamento. Processos recentes têm muitos censurados, e misturá-los com antigos sem o modelo certo distorce a comparação.
6. Para comparar grupos controlando outras variáveis, o modelo de Cox, com a checagem de riscos proporcionais, cabe melhor que uma regressão do tempo dos encerrados.

## Taxas e comparações

- Defina o denominador: procedência sobre sentenças de mérito, reforma sobre recursos julgados, acordo sobre audiências realizadas.
- Toda proporção vem com o número de casos e um intervalo, como o de Wilson. Abaixo de algumas dezenas de casos por grupo, relate como sem conclusão.
- Compare unidades dentro da mesma classe e assunto e no mesmo período. Ajuste pelo volume e pela composição de casos antes de dizer que uma é mais lenta ou mais favorável.
- Rankings de juízes ou de relatores pelo nome são dados sobre pessoas e incentivam uso indevido: mostre unidades, e só nomeie julgadores com decisão do usuário e finalidade registrada.

## Classificação de decisões

- Uma regra de texto ou um modelo que classifica decisões (procedente, improcedente, parcialmente procedente, extinção sem mérito) é validado numa amostra aleatória estratificada, lida à mão por quem conhece o direito, com a taxa de acerto por classe e a matriz de confusão.
- Procedência parcial e extinção sem mérito são os erros mais comuns; mantenha-os como categorias próprias.
- Antes de mandar texto de decisões a um LLM ou a uma API externa, siga a `personal-data`: as decisões têm nomes e dados das partes.

## Previsões

- O instante da previsão define o que entra: só movimentos e documentos anteriores a ele.
- Valide fora do tempo: treine com processos mais antigos e teste com os mais recentes.
- A saída de uma previsão para um caso diz que é estimativa, mostra o número de casos semelhantes e o intervalo, e deixa a decisão com quem responde pelo caso.

## Fontes

Conferidas em 08/11/2026:

- Resolução CNJ 46/2007: https://atos.cnj.jus.br/atos/detalhar/167
- SGT, consulta pública e versões: https://www.cnj.jus.br/sgt/consulta_publica_classes.php e https://www.cnj.jus.br/sgt/versoes.php

Documentação dos pacotes, para conferir a função na versão instalada:

- `survival` no CRAN: https://cran.r-project.org/package=survival
- `lifelines`: https://lifelines.readthedocs.io/
