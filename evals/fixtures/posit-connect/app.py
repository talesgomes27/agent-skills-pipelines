from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("Vendas por região"),
    ui.input_select("regiao", "Região", ["Norte", "Sul", "Leste", "Oeste"]),
    ui.output_text("total"),
)

TOTAIS = {"Norte": 120.0, "Sul": 340.5, "Leste": 98.2, "Oeste": 210.0}


def server(input, output, session):
    @render.text
    def total():
        return f"Total: {TOTAIS[input.regiao()]:.2f}"


app = App(app_ui, server)
