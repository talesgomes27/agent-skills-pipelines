from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/pedidos", status_code=201)
def criar(pedido: dict):
    if pedido["valor"] < 0:
        raise HTTPException(status_code=422, detail="valor negativo")
    return pedido
