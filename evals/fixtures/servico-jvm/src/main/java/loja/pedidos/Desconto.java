package loja.pedidos;

public class Desconto {
    /** Aplica o percentual de desconto e devolve o valor em reais, com duas casas. */
    public static double aplicar(double valor, double percentual) {
        double comDesconto = valor * (1 - percentual / 100);
        return Math.floor(comDesconto * 100) / 100;
    }
}
