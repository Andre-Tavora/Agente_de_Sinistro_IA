from fastapi import FastAPI
from app.routers import sinistro, vistoria, apolice

app = FastAPI(title="Agente de Sinistro IA")

app.include_router(sinistro.router)
app.include_router(vistoria.router)
app.include_router(apolice.router)


@app.get("/")
def root():
    return {"status": "ok"}
