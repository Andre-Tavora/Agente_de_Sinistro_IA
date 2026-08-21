from fastapi import FastAPI, Depends
from app.auth import verify_token
from app.schemas import Apolice

app = FastAPI(title="Agente de Sinistro IA")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/apolice/{numero}", response_model=Apolice)
def get_apolice(numero: str, token: str = Depends(verify_token)):
    return Apolice(
        numero=numero,
        segurado="Mock Segurado",
        cobertura="Roubo/Furto",
        vigencia_inicio="2026-01-01",
        vigencia_fim="2026-12-31"
    )
