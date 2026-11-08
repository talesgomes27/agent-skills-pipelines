library(shiny)
library(dplyr)
library(ggplot2)

# app.R único: cresceu sem módulos

ui <- navbarPage("Painel de vendas",
  tabPanel("Receita",
    sidebarLayout(
      sidebarPanel(
        selectInput("receita_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("receita_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("receita_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("receita_grafico"),
        tableOutput("receita_tabela"),
        textOutput("receita_resumo")
      )
    )
  ),
  tabPanel("Pedidos",
    sidebarLayout(
      sidebarPanel(
        selectInput("pedidos_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("pedidos_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("pedidos_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("pedidos_grafico"),
        tableOutput("pedidos_tabela"),
        textOutput("pedidos_resumo")
      )
    )
  ),
  tabPanel("Ticket",
    sidebarLayout(
      sidebarPanel(
        selectInput("ticket_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("ticket_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("ticket_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("ticket_grafico"),
        tableOutput("ticket_tabela"),
        textOutput("ticket_resumo")
      )
    )
  ),
  tabPanel("Clientes",
    sidebarLayout(
      sidebarPanel(
        selectInput("clientes_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("clientes_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("clientes_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("clientes_grafico"),
        tableOutput("clientes_tabela"),
        textOutput("clientes_resumo")
      )
    )
  ),
  tabPanel("Devolucoes",
    sidebarLayout(
      sidebarPanel(
        selectInput("devolucoes_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("devolucoes_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("devolucoes_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("devolucoes_grafico"),
        tableOutput("devolucoes_tabela"),
        textOutput("devolucoes_resumo")
      )
    )
  ),
  tabPanel("Frete",
    sidebarLayout(
      sidebarPanel(
        selectInput("frete_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("frete_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("frete_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("frete_grafico"),
        tableOutput("frete_tabela"),
        textOutput("frete_resumo")
      )
    )
  ),
  tabPanel("Margem",
    sidebarLayout(
      sidebarPanel(
        selectInput("margem_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("margem_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("margem_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("margem_grafico"),
        tableOutput("margem_tabela"),
        textOutput("margem_resumo")
      )
    )
  ),
  tabPanel("Estoque",
    sidebarLayout(
      sidebarPanel(
        selectInput("estoque_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("estoque_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("estoque_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("estoque_grafico"),
        tableOutput("estoque_tabela"),
        textOutput("estoque_resumo")
      )
    )
  ),
  tabPanel("Atrasos",
    sidebarLayout(
      sidebarPanel(
        selectInput("atrasos_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("atrasos_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("atrasos_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("atrasos_grafico"),
        tableOutput("atrasos_tabela"),
        textOutput("atrasos_resumo")
      )
    )
  ),
  tabPanel("Nps",
    sidebarLayout(
      sidebarPanel(
        selectInput("nps_regiao", "Região", choices = c("Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste")),
        dateRangeInput("nps_periodo", "Período", start = "2025-01-01", end = "2025-12-31"),
        checkboxInput("nps_acumulado", "Acumulado", FALSE)
      ),
      mainPanel(
        plotOutput("nps_grafico"),
        tableOutput("nps_tabela"),
        textOutput("nps_resumo")
      )
    )
  )
)

server <- function(input, output, session) {
  # ---- receita ----
  dados_receita <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$receita_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$receita_periodo[1] & as.Date(vendas$data) <= input$receita_periodo[2], ]
    vendas
  })
  output$receita_grafico <- renderPlot({
    d <- dados_receita()
    if (input$receita_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$receita_tabela <- renderTable({
    d <- dados_receita()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$receita_resumo <- renderText({
    d <- dados_receita()
    paste("Total de receita:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$receita_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })

  # ---- pedidos ----
  dados_pedidos <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$pedidos_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$pedidos_periodo[1] & as.Date(vendas$data) <= input$pedidos_periodo[2], ]
    vendas
  })
  output$pedidos_grafico <- renderPlot({
    d <- dados_pedidos()
    if (input$pedidos_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$pedidos_tabela <- renderTable({
    d <- dados_pedidos()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$pedidos_resumo <- renderText({
    d <- dados_pedidos()
    paste("Total de pedidos:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })

  # ---- ticket ----
  dados_ticket <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$ticket_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$ticket_periodo[1] & as.Date(vendas$data) <= input$ticket_periodo[2], ]
    vendas
  })
  output$ticket_grafico <- renderPlot({
    d <- dados_ticket()
    if (input$ticket_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$ticket_tabela <- renderTable({
    d <- dados_ticket()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$ticket_resumo <- renderText({
    d <- dados_ticket()
    paste("Total de ticket:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$ticket_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })

  # ---- clientes ----
  dados_clientes <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$clientes_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$clientes_periodo[1] & as.Date(vendas$data) <= input$clientes_periodo[2], ]
    vendas
  })
  output$clientes_grafico <- renderPlot({
    d <- dados_clientes()
    if (input$clientes_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$clientes_tabela <- renderTable({
    d <- dados_clientes()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$clientes_resumo <- renderText({
    d <- dados_clientes()
    paste("Total de clientes:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$clientes_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })

  # ---- devolucoes ----
  dados_devolucoes <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$devolucoes_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$devolucoes_periodo[1] & as.Date(vendas$data) <= input$devolucoes_periodo[2], ]
    vendas
  })
  output$devolucoes_grafico <- renderPlot({
    d <- dados_devolucoes()
    if (input$devolucoes_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$devolucoes_tabela <- renderTable({
    d <- dados_devolucoes()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$devolucoes_resumo <- renderText({
    d <- dados_devolucoes()
    paste("Total de devolucoes:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })

  # ---- frete ----
  dados_frete <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$frete_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$frete_periodo[1] & as.Date(vendas$data) <= input$frete_periodo[2], ]
    vendas
  })
  output$frete_grafico <- renderPlot({
    d <- dados_frete()
    if (input$frete_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$frete_tabela <- renderTable({
    d <- dados_frete()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$frete_resumo <- renderText({
    d <- dados_frete()
    paste("Total de frete:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$frete_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })

  # ---- margem ----
  dados_margem <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$margem_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$margem_periodo[1] & as.Date(vendas$data) <= input$margem_periodo[2], ]
    vendas
  })
  output$margem_grafico <- renderPlot({
    d <- dados_margem()
    if (input$margem_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$margem_tabela <- renderTable({
    d <- dados_margem()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$margem_resumo <- renderText({
    d <- dados_margem()
    paste("Total de margem:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$margem_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })

  # ---- estoque ----
  dados_estoque <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$estoque_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$estoque_periodo[1] & as.Date(vendas$data) <= input$estoque_periodo[2], ]
    vendas
  })
  output$estoque_grafico <- renderPlot({
    d <- dados_estoque()
    if (input$estoque_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$estoque_tabela <- renderTable({
    d <- dados_estoque()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$estoque_resumo <- renderText({
    d <- dados_estoque()
    paste("Total de estoque:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$estoque_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })

  # ---- atrasos ----
  dados_atrasos <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$atrasos_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$atrasos_periodo[1] & as.Date(vendas$data) <= input$atrasos_periodo[2], ]
    vendas
  })
  output$atrasos_grafico <- renderPlot({
    d <- dados_atrasos()
    if (input$atrasos_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$atrasos_tabela <- renderTable({
    d <- dados_atrasos()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$atrasos_resumo <- renderText({
    d <- dados_atrasos()
    paste("Total de atrasos:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })

  # ---- nps ----
  dados_nps <- reactive({
    vendas <- read.csv("data/vendas.csv")
    Sys.sleep(1)
    vendas <- vendas[vendas$regiao == input$nps_regiao, ]
    vendas <- vendas[as.Date(vendas$data) >= input$nps_periodo[1] & as.Date(vendas$data) <= input$nps_periodo[2], ]
    vendas
  })
  output$nps_grafico <- renderPlot({
    d <- dados_nps()
    if (input$nps_acumulado) d$valor <- cumsum(d$valor)
    ggplot(d, aes(as.Date(data), valor)) + geom_line()
  })
  output$nps_tabela <- renderTable({
    d <- dados_nps()
    d %>% group_by(mes = substr(data, 1, 7)) %>% summarise(total = sum(valor))
  })
  output$nps_resumo <- renderText({
    d <- dados_nps()
    paste("Total de nps:", format(sum(d$valor), big.mark = "."))
  })
  observeEvent(input$nps_regiao, {
    # cópia 1 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 2 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 3 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 4 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 5 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })

  observeEvent(input$receita_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$receita_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("receita: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$pedidos_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("pedidos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$ticket_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("ticket: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$clientes_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("clientes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$devolucoes_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("devolucoes: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$frete_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("frete: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$margem_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("margem: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$estoque_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("estoque: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$atrasos_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("atrasos: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 6 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 7 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 8 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 9 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 10 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 11 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 12 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 13 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 14 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 15 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 16 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 17 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 18 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 19 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 20 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 21 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
  observeEvent(input$nps_regiao, {
    # cópia 22 do mesmo cálculo, deixada por versões antigas
    vendas <- read.csv("data/vendas.csv")
    message("nps: ", nrow(vendas), " linhas")
  })
}

shinyApp(ui, server)
