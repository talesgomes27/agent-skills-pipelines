---
name: jurimetria
description: "Use quando o trabalho envolve dados de processos judiciais brasileiros: validar, cruzar ou contar números de processo do CNJ, API Pública do DataJud, classes, assuntos ou movimentos das Tabelas Processuais Unificadas, tempo de tramitação, taxas de decisão, sentenças ou acórdãos para classificar, ou jurimetria."
---

# Jurimetria

Dados de processos judiciais têm regras próprias: um identificador com dígito verificador, tabelas oficiais de classes e movimentos, uma API pública com termos de uso, sigilo processual e métodos que erram com facilidade. Esta skill dá essas regras. Ela informa as pipelines: escopo, gates e autorizações continuam os delas. Não é aconselhamento jurídico, e a conclusão sobre um caso concreto é de quem responde por ele.

## Número único de processo

- O formato é `NNNNNNN-DD.AAAA.J.TR.OOOO` (Resolução CNJ 65/2008): sequencial, dígito verificador, ano do ajuizamento, segmento da Justiça, tribunal e unidade de origem. Detalhes e códigos em [número único](references/numero-cnj.md).
- Antes de cruzar, contar ou deduplicar, normalize para os 20 dígitos sem máscara e valide o dígito com `scripts/numero_cnj.py`, ou com `abjutils::verify_cnj` em R. Guarde o número sem máscara e formate só na saída.
- Número inválido vai para uma lista à parte, com a contagem no relatório. Nunca corrija adivinhando o dígito ou o sequencial, e nunca conte um inválido como "não encontrado" na outra base.
- Redistribuição para outro tribunal gera número novo, e no mesmo tribunal não; a execução penal mantém o número. Cruzar bases de tribunais diferentes pelo número pode perder o processo que mudou de tribunal; diga isso no relatório.

## Fontes, na ordem de preferência

1. API Pública do DataJud, do CNJ: metadados de processos de todos os tribunais (classe, assuntos, movimentos, órgão julgador, grau), sem partes, sem advogados e sem o inteiro teor. Como pedir, paginar e o que ela não traz está em [DataJud](references/datajud.md).
2. Dados abertos e painéis oficiais dos tribunais e do CNJ.
3. Consulta pública dos tribunais, só quando as duas primeiras não bastam, pelas regras de coleta externa da `execution-pipeline`: termos de uso, ritmo baixo e parar diante de CAPTCHA, nunca contorná-lo.

- A chave da API é pública e o CNJ pode trocá-la a qualquer momento: leia-a na página de acesso da wiki do DataJud e guarde-a na configuração do projeto, não no código.
- O uso da API é só para fins legais e não comerciais, até 120 requisições por minuto, e citar o CNJ e o DataJud como fontes é obrigatório em publicações, painéis, aplicativos e estudos. Ponha a citação nessas saídas e o limite no código de coleta.
- Dados obtidos por acesso funcional a sistemas internos do tribunal ficam fora por padrão: só entram com decisão do usuário, dentro da finalidade dessa função.
- A API está em fase beta e reflete o que cada tribunal remeteu ao CNJ. Diga a data da coleta e trate lacunas de um tribunal como lacuna da remessa, não como ausência de processos.

## Códigos, não nomes

- Classes, assuntos e movimentos seguem as Tabelas Processuais Unificadas (Resolução CNJ 46/2007), consultadas e baixadas no Sistema de Gestão de Tabelas (SGT) do CNJ. Agrupe e filtre pelo código, nunca pelo nome: o mesmo código aparece com grafias diferentes entre tribunais e versões.
- Registre a versão da tabela usada. Assuntos e movimentos podem ter complementos locais do tribunal; trate os locais à parte e diga quantos são.

## Tempo de tramitação

- Defina com o usuário, antes de calcular, o início (em geral o ajuizamento), o evento de fim (o código do movimento no SGT, como a baixa definitiva ou o julgamento) e a data de corte da coleta.
- Processo ainda em curso na data de corte é observação censurada: ele entra na análise com o tempo até o corte. Descartá-lo encurta a estimativa, porque os casos longos são justamente os que não terminaram.
- Use análise de sobrevivência: curva de Kaplan-Meier e mediana com intervalo, por classe ou unidade, com o pacote `survival` em R ou `lifelines` em Python. Média dos encerrados não é tempo de tramitação.
- Coorte por ano de ajuizamento evita comparar processos novos, que ainda não tiveram tempo de terminar, com antigos. O método está em [métodos](references/metodos.md).

## Comparações justas

- Uma vara ou comarca mais lenta, ou com mais procedências, não é "pior" antes de controlar classe, assunto, volume e o período. Compare dentro do mesmo tipo de ação.
- Taxas precisam do denominador certo, como procedências sobre sentenças de mérito, e não sobre todos os processos. Proporção vem com o número de casos e um intervalo, e grupo pequeno é relatado como sem conclusão.
- Associação não é causa, e uma diferença entre julgadores identificados é dado sobre pessoas: saídas mostram unidades, não nomes de juízes, salvo decisão do usuário com finalidade clara, seguindo as regras de perfilamento da `personal-data`.

## Modelos e previsões

- Para prever duração ou resultado, só entram informações disponíveis no instante da previsão. Movimentos posteriores, como trânsito em julgado ou arquivamento, revelam o fim e vazam o resultado.
- Uma estimativa de chance para um caso concreto sai como estimativa, com o número de casos semelhantes e o intervalo, e diz que a decisão é de quem responde pelo caso. Nada de ajuste "por julgamento" do agente sobre o número calculado.

## Texto de decisões

- Classificar sentenças ou acórdãos por regra ou por modelo pede validação: uma amostra aleatória lida à mão, com a taxa de acerto e os erros típicos no relatório, antes de usar a classificação nas contagens.
- Decisões trazem nomes, CPF e endereços de partes: carregue a `personal-data`. Esses dados saem da análise e das saídas, que mostram só agregados.

## Sigilo

- Processo em segredo de justiça fica fora por padrão, mesmo que o arquivo do usuário o traga. Só entra quando o usuário é parte ou procurador nele (CPC, art. 189) e decide incluí-lo com a finalidade registrada, e mesmo assim as saídas mostram só agregados.
- No DataJud, os processos em segredo têm os dados excluídos ou anonimizados (Portaria CNJ 160/2020, com a redação da Portaria 374/2026). Trate `nivelSigilo` acima de zero como sigiloso, por cautela, porque o glossário só diz "nível de sigilo", e diga quantos saíram.
- Dado anonimizado pela fonte continua sensível: não tente reidentificar cruzando bases.

## Especialistas e ferramentas

- `scripts/numero_cnj.py` valida e normaliza números (biblioteca padrão, sem rede); em R, o `abjutils` da Associação Brasileira de Jurimetria faz o mesmo e mais.
- As pipelines carregam esta skill quando as fontes do trabalho são judiciais, a lacuna concreta que ela cobre; a `personal-data` vale junto sempre que houver partes; a coleta externa segue a `execution-pipeline`.
- Fatos de norma e de plataforma mudam. As referências trazem o link oficial e a data em que cada fato foi conferido; reconfira antes de publicar um resultado.
