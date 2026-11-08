package loja.pedidos;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class DescontoTest {
    @Test
    void dezPorCento() {
        assertEquals(90.0, Desconto.aplicar(100.0, 10.0));
    }
}
