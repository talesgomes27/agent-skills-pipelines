---
name: humanizer
description: "Reescreve textos, commits e documentações com voz sênior, variação métrica de ritmo (burstiness) e eliminação de vícios e clichês de IA."
license: MIT
metadata:
  version: "3.1.0"
---

# Humanizer: Redação Humana e Prevenção de Padrões de IA

Escreva ou reescreva textos, documentações, mensagens de commit e interfaces para que soem como um profissional experiente e autêntico, e não como um modelo de linguagem artificial (LLM). Mantenha rigorosamente todos os fatos, dados e requisitos técnicos; elimine a afetação, a fórmula padronizada e os vícios estruturais de IA.

---

## 1. Como Funcionam os Detectores de IA e Como Evitá-los

De acordo com pesquisas acadêmicas (Stanford, MIT, Weber-Wulff et al., 2023) e o artigo da Wikipédia lusófona sobre *Detecção de conteúdo gerado por inteligência artificial*, ferramentas de detecção (Turnitin, GPTZero, Copyleaks) e avaliadores humanos buscam padrões estatísticos previsíveis:

1. **Baixa Perplexidade**: Modelos de linguagem sempre escolhem a palavra estatisticamente mais provável e genérica. Textos humanos contêm vocabulário específico, técnico, imperfeito e vocacionado ao contexto.
2. **Baixa Variação de Ritmo (*Low Burstiness*)**: LLMs tendem a produzir frases com contagem de palavras e complexidade sintática quase uniformes (geralmente entre 14 e 22 palavras por frase). Humanos escrevem em rajadas: intercalam frases telegráficas de 3 a 6 palavras com períodos longos e articulados.
3. **Simetria Rígida**: Listas onde cada item possui exatamente um título em negrito com dois pontos seguido por uma frase de 15 palavras; seções que sempre fecham com um parágrafo reflexivo de duas frases.
4. **Falsos Positivos em Avaliações de Portfólio**: Avaliadores e recrutadores desconfiam de portfólios que usam prosa enciclopédica ou tom de redação escolar para descrever códigos. Um desenvolvedor sênior descreve decisões arquiteturais de forma sóbria e pragmática.

### Diretrizes Centrais Antidetecção:
* **Alterne o comprimento das sentenças de forma intencional**. Escreva uma frase curta e contundente. Em seguida, elabore uma sentença mais longa explicando as razões técnicas, sem medo de variar o ritmo.
* **Corte a simetria de listas**. Quando fizer tópicos, nem todo item precisa de negrito inicial ou do mesmo comprimento.
* **Prefira termos específicos a sinônimos corporativos genéricos**. Em vez de *"solução robusta e escalável"*, diga *"pipeline em Python com processamento em lote e tolerância a falhas"*.
* **Corte conclusões moralizantes ou de fechamento óbvio**. Termine o texto no último fato concreto útil.

---

## 2. Princípios de Redação em Português e Inglês

### A. Eliminação de Gerundismos Vazios e Riders em -ing
* **Evite**: *"destacando a importância de"*, *"reforçando o compromisso com"*, *"evidenciando a necessidade de"*, *"contribuindo para o avanço de"*, *"garantindo assim uma experiência fluida"*.
* **Substitua por**: O fato direto em voz ativa ou corte a oração subordinada.
  * *Antes*: *"O sistema utiliza cache local, garantindo assim uma experiência de alta performance e resiliência."*
  * *Depois*: *"O sistema utiliza cache local para carregar os dados offline caso a conexão falhe."*

### B. Proibição de Contrastes Falsos ("Não X, mas Y")
* **Evite**: *"Não se trata apenas de X, mas de Y"*, *"Mais do que um simples dashboard, uma central de inteligência"*, *"It's not just about X, it's a statement"*.
* **Substitua por**: A afirmação positiva direta.
  * *Antes*: *"Isso não significa apenas refatorar código, mas repensar a arquitetura."*
  * *Depois*: *"A refatoração modularizou a aplicação e eliminou dependências obsoletas."*

### C. Fim das Tríades Forçadas
* **Evite**: A compulsão de sempre citar três itens para soar equilibrado (*"inovação, agilidade e escalabilidade"*; *"projetado para aprender, evoluir e transformar"*).
* **Substitua por**: Cite apenas os itens reais necessários (um, dois ou quatro).

### D. Banimento de Travessões Excessivos (`—`)
* **Regra**: Não use travessões duplos (`—` ou `--`) como conectores universais entre orações. Substitua por vírgula, ponto final, dois-pontos ou parênteses, ou reestruture a oração.

### E. Vocabulário Clichê de IA (Lista Negra)
Corte ou substitua estes termos quando usados de forma figurativa ou empolada:
* **Português**: *robusto*, *crucial*, *vital*, *ecossistema*, *panorama*, *testemunho*, *revolucionário*, *fascinante*, *profundo*, *reengenharia completa*, *pioneiro*, *orquestração perfeita*, *desafios e perspectivas futuras*, *um passo fundamental*.
* **Inglês**: *delve*, *deep dive*, *crucial*, *pivotal*, *testament*, *tapestry*, *landscape*, *vibrant*, *fostering*, *underscoring*, *showcasing*, *nuance*, *robust* (figurativo).

---

## 3. Diretrizes Específicas por Tipo de Documento

### 3.1. Mensagens de Commit no Git
* Use o formato **Conventional Commits** em minúsculas e sem pontuação final no título:
  * `feat: adiciona tour de eventos historicos e analise de sazonalidade`
  * `fix: corrige timeout de conexao na ingestao da api`
  * `docs: atualiza instrucoes de instalacao no readme`
  * `refactor: modulariza funcoes graficas em plots.R`
* **Nunca use**:
  * Adjetivos promocionais no commit (*"modernização espetacular"*, *"código incrivelmente limpo"*).
  * Menções a prompts, IAs ou ferramentas geradoras.
  * Emojis no commit a menos que o projeto adote `gitmoji` expressamente.

### 3.2. Documentações (`README.md`, Arquitetura, ADRs)
* Abra direto com a função do software e como executá-lo.
* Explique problemas técnicos reais (ex: *"a biblioteca X impedia o build em WebAssembly"* em vez de *"o código legado sofria com débito técnico inaceitável"*).
* Não decore todo título com emojis (ex: use `## Arquitetura` em vez de `## 🏛️✨ Arquitetura Revolucionária`).
* Mantenha equações matemáticas, referências bibliográficas e comandos limpos.

### 3.3. Interfaces com Usuário (UI / Front-End)
* Rótulos curtos e acionáveis: `Filtros`, `Exportar CSV`, `Dados Históricos` (em vez de *"Controles Centrais da Missão"*).
* Banners explicativos com dados objetivos, sem tom dramático de documentário de TV.

---

## 4. O Checklist do Humanizador

Antes de finalizar qualquer texto, faça a leitura e verifique:
1. [ ] Há algum contraste *"não apenas X, mas Y"*?
2. [ ] Há travessões (`—`) conectando ideias que deveriam ser frases separadas?
3. [ ] Há listas simétricas onde todos os itens foram formatados com negrito decorativo?
4. [ ] O texto parece estar tentando impressionar o leitor em vez de transmitir uma informação técnica?
5. [ ] O tamanho das frases varia de forma perceptível (*burstiness*)?
6. [ ] A mensagem soa como a fala de um engenheiro/cientista de dados no terminal?
