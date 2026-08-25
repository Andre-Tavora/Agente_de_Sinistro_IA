from fastapi import APIRouter, Depends, HTTPException
from app.auth import verify_token
from app.schemas import Apolice
from app.services.apolice_client import consultar_apolice

router = APIRouter(prefix="/apolice", tags=["apolice"])


@router.get("/{numero_apolice}", response_model=Apolice)
def get_apolice(numero_apolice: str, token: str = Depends(verify_token)):
    try:
        return consultar_apolice(numero_apolice)
    except ValueError as e:
        msg = str(e)
        status = 404 if "não encontrada" in msg else 503
        raise HTTPException(status_code=status, detail=msg) from e
