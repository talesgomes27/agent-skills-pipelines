# ETL de pedidos (fixture sintética)

Lê `entrada/pedidos.csv` todo dia às 2h (ver `crontab`) e grava em `saida/pedidos.parquet`, acrescentando as linhas do dia.
O deploy de ontem (versão 1.4.0) trocou o leitor de datas.
