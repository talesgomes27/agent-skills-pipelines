# Exemplos Antes/Depois

## 1. Introdução de PRD

Antes:
  "O presente documento tem como objetivo crucial apresentar uma
   visão abrangente e inovadora da plataforma de pagamentos,
   destacando a importância vital de transformar a experiência do
   usuário por meio de uma orquestração perfeita entre resiliência e
   alta performance."

Depois:
  "Este PRD especifica o novo serviço de pagamentos PIX e cartão. O
   objetivo é reduzir o tempo de liquidação para menos de 400
   milissegundos e suportar até 2.500 transações por segundo em
   horários de pico."

## 2. Docstring de Função

Antes:
  """Esta função é responsável por realizar o parsing eficiente e
     robusto de strings de data, garantindo assim que o sistema
     manipule timestamps de forma harmoniosa e sem falhas
     inesperadas."""

Depois:
  """Converte string ISO 8601 em datetime timezone-aware (UTC).

  Args:
      date_str: Data no formato 'YYYY-MM-DDTHH:MM:SSZ'.
  Returns:
      Instância de datetime normalizada em UTC.
  Raises:
      ValueError: Se a string não contiver o formato ISO válido.
  """

## 3. Resultados em Relatório Quarto

Antes:
  "Ao analisar os dados da Figura 2, é fascinante notar não apenas
   uma tendência clara de alta, mas também um salto extraordinário
   nas métricas, o que evidencia de maneira inquestionável o
   compromisso da nova abordagem com a excelência operacional."

Depois:
  "As vendas cresceram 18,4% no terceiro trimestre, totalizando R$
   4,2 milhões (Figura 2). O aumento decorreu da entrada de 120 novos
   clientes corporativos no segmento B2B. A taxa de churn permaneceu
   estável em 2,1%."

## 4. Getting Started de README

Antes:
  "Para embarcar na jornada de execução deste ecossistema
   revolucionário, é fundamental seguir alguns passos preparatórios
   simples, configurando de forma harmoniosa o ambiente local para
   obter o máximo proveito da aplicação."

Depois:
  "### Instalação Rápida
   Requisitos: Python 3.12+ e Docker.
   ```bash
   git clone https://github.com/empresa/servico.git && cd servico
   cp .env.example .env
   docker compose up -d
   uv run pytest
   ```"

## 5. Mensagem de Erro de CLI

Antes:
  "Ops! Lamentamos informar que algo inesperado aconteceu durante a
   orquestração do seu comando. Parece que o arquivo especificado não
   pôde ser localizado no diretório atual. Por favor, verifique se o
   caminho digitado está correto e tente novamente mais tarde!"

Depois:
  "erro: arquivo 'config.yaml' não encontrado em /etc/app/. Use
   --config <path> para indicar um arquivo válido."
