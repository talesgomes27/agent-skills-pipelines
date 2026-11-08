from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_r003_valor_negativo():
    client.post("/pedidos", json={"cliente_id": 1, "valor": -5})


def test_r001_cria_pedido():
    r = client.post("/pedidos", json={"cliente_id": 1, "valor": 10})
    assert r.status_code == 201
