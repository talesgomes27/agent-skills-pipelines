---
name: personal-data
description: "Use quando o trabalho lê, transforma, mostra, guarda ou envia dados que identificam pessoas (CPF, nome, e-mail, telefone, endereço, notas, saúde; de clientes, usuários, alunos, funcionários ou pacientes), ou documentos que possam contê-los, mesmo que o pedido principal seja outro: análises, relatórios, dashboards, apps, listas, logs, formulários, coletas, envio a LLM ou API externa, LGPD."
---

# Dados pessoais

Dado pessoal é qualquer informação ligada a uma pessoa identificada ou identificável (LGPD, art. 5, I). Esta skill dá as regras práticas para tratar esses dados num trabalho técnico. Ela informa as pipelines: escopo, gates e autorizações continuam os delas. Não é aconselhamento jurídico. Base legal, contratos e comunicação de incidente são decisões de quem responde pelos dados na organização; o agente aponta a decisão em vez de tomá-la.

## Inventário

- Lendo só o cabeçalho ou o esquema, antes de carregar os valores, liste os campos pessoais: identificadores diretos (CPF, nome, e-mail, telefone, endereço, número de documento ou de cliente) e indiretos que, juntos, identificam alguém, como CEP com data de nascimento ou cidade pequena com profissão.
- Marque os dados sensíveis (saúde, origem racial ou étnica, religião, opinião política, filiação sindical, vida sexual, genética, biometria) e os de crianças e adolescentes. Eles pedem o esforço rigoroso.
- Registre a finalidade do trabalho e use só os dados que ela pede. Se a finalidade não está clara, ou parece diferente daquela para a qual os dados foram coletados, pergunte ao usuário antes de usá-los.

## Minimização

- Leia só os campos necessários e tire os identificadores diretos antes da análise quando ela não precisa deles.
- Numa análise única, deduplique em memória pelo identificador normalizado, sem gravá-lo, e descarte-o logo depois.
- Quando o pseudônimo precisa persistir, para juntar tabelas ou execuções diferentes, use um HMAC com uma chave que fica com o usuário ou no cofre do projeto, fora do código e do repositório. Hash simples de CPF, sem chave, é revertido por força bruta, porque há poucos CPFs possíveis.
- Dado pseudonimizado continua sendo dado pessoal. Só é anonimizado o que não permite identificar a pessoa por meios técnicos razoáveis; tirar o nome não basta.
- Validação e limpeza de identificadores (CPF válido, formato de e-mail, duplicados) rodam antes da pseudonimização, e o registro da limpeza traz contagens, nunca valores.

## Saídas

- Saídas de análise (slides, relatórios, dashboards analíticos, resumos por e-mail) mostram agregados. Nenhuma linha real, exemplo de cliente ou identificador aparece nelas.
- Telas e listas operacionais, em que mostrar a pessoa é o objetivo, como o cadastro de um cliente ou a lista que o CRM vai contatar, mostram só os campos necessários a quem tem acesso e seguem as regras de envio abaixo.
- Um grupo com menos pessoas que o mínimo aprovado pelo usuário é juntado a outro ou omitido, porque o recorte identifica quem está nele. Proponha o mínimo no plano, por exemplo 5 ou 10.
- Score ou ranking de pessoas, como risco de churn ou de crédito, é perfilamento. A lista diz que o score é estimativa e a quem pedir a revisão de uma decisão, o plano define quantos nomes vão e se o score aparece, e uma decisão sobre alguém tomada só pelo modelo precisa permitir revisão humana. Modelo que pontua ou ordena pessoas mede o viés por grupo antes de liberar e em cada execução em produção, como em [viés de modelo](references/model-fairness.md).
- Gráficos não rotulam pontos individuais, e tabelas exportáveis respeitam a política de acesso aprovada.
- Saídas de notebook com linhas pessoais são limpas antes de versionar ou publicar.

## Onde os dados ficam

- Dado bruto e dado limpo ficam fora do Git, num caminho que o plano nomeia e que o `.gitignore` cobre. A fonte original fica como está; as cópias temporárias que você criou são apagadas no fim, e o relatório diz onde os dados ficaram.
- Logs, mensagens de erro, resumos e alertas de job não mostram valores pessoais: registre contagens e identificadores pseudonimizados.
- Testes usam dados sintéticos ou mascarados. Uma cópia de produção para ensaio recebe a mesma proteção do original e é apagada depois.

## Envio e compartilhamento

- Mandar dados pessoais para fora do ambiente do projeto é decisão do usuário, tomada antes do envio, sabendo o que vai, para quem e por quanto tempo fica lá. Isso vale para provedor de LLM, API externa, e-mail, planilha compartilhada e plataforma de nuvem ou de CI, como o GitHub Actions. Provedor fora do Brasil faz transferência internacional, e os termos dele dizem se guarda os dados ou os usa para treino; as duas coisas entram na decisão.
- Mande só o necessário e, quando der, sem identificadores. Num app com LLM, os documentos e as perguntas dos usuários também são dados enviados ao provedor. Num servidor MCP ou agente com acesso a um banco de pessoas, a ferramenta devolve só as colunas que a pergunta precisa, com CPF e contatos mascarados, e o texto livre que ela devolve é dado, não instrução; o código do servidor segue a `execution-pipeline`.
- Documento interno pode não ter dados pessoais e ainda ser confidencial. O envio a terceiros pede a decisão do usuário nos dois casos; pergunte também se os documentos têm dados de pessoas.
- Perguntas que um app guarda são dados de quem pergunta. O plano define se ficam, por quanto tempo, quem as lê e como os usuários são avisados.
- Uma lista operacional com dados pessoais, como os clientes que o CRM vai contatar, vai por um canal de acesso restrito, como o próprio CRM ou uma pasta com acesso controlado, em vez de anexo de e-mail, e só com os campos que quem recebe usa. O plano diz quem recebe e por quanto tempo a lista vale. Contato direto com as pessoas da lista respeita as preferências que elas já registraram, como pedir para não ser contatadas; confirme com o usuário de onde vêm essas preferências.

## Coleta

- Formulário ou coleta nova pede só o necessário e diz à pessoa para que o dado serve. Consentimento, aviso e prazo de guarda são decisões do responsável pelos dados.
- Coleta em sites de terceiros segue as regras de coleta externa da `execution-pipeline`, e o dado pessoal coletado entra no inventário.

## Vazamento

Se um dado pessoal apareceu onde não devia (commit, log, saída publicada, mensagem enviada), pare e diga ao usuário onde está, sem repetir o valor. Não reescreva histórico nem apague por conta própria: remover a linha não desfaz a exposição, e comunicar o incidente cabe ao controlador.

## Especialistas e ferramentas

Para procurar dados pessoais em texto ou tabelas, o Microsoft Presidio é uma opção quando estiver instalado; um detector automático dá candidatos, não garantia. Os pontos da lei citados aqui estão em [LGPD para o trabalho técnico](references/lgpd-basics.md).
