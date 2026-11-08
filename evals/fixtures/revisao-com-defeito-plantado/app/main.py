from fastapi import FastAPI

from app.pedidos import router

app = FastAPI()
app.include_router(router)
