from fastapi import FastAPI, Depends, HTTPException
from app.auth import verify_token
from app.schemas import Apolice
from app.mock_data import APOLICES
from app.routers import sinistro, vistoria

app = FastAPI(title="Agente de Sinistro IA")

app.include_router(sinistro.router)
app.include_router(vistoria.router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/apolice/{numero}", response_model=Apolice)
def get_apolice(numero: str, token: str = Depends(verify_token)):
    apolice = APOLICES.get(numero)
    if not apolice:
        raise HTTPException(status_code=404, detail="Apólice não encontrada")
    return apolice
