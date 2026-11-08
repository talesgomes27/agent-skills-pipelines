import pandas as pd
import streamlit as st


def filtrar(vendas: pd.DataFrame, regioes: list[str]) -> pd.DataFrame:
    return vendas[vendas["regiao"].isin(regioes)] if regioes else vendas


def main():
    vendas = pd.read_csv("dados/vendas_exemplo.csv")
    regioes = st.multiselect("Região", sorted(vendas["regiao"].unique()))
    selecao = filtrar(vendas, regioes)
    st.metric("Total da seleção", f"{selecao['valor'].sum():.2f}")
    st.dataframe(selecao)


if __name__ == "__main__":
    main()
