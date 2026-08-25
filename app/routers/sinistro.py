from fastapi import APIRouter, Depends, HTTPException
from app.auth import verify_token
from app.schemas import Sinistro
from app.services.sinistro_client import consultar_sinistro, abrir_sinistro
from pydantic import BaseModel

router = APIRouter(prefix="/sinistro", tags=["sinistro"])


class AberturaSinistroRequest(BaseModel):
    numero_apolice: str
    tipo: str
    descricao: str


def _tratar_erro(e: ValueError) -> HTTPException:
    msg = str(e)
    status = 404 if "não encontrada" in msg or "não encontrado" in msg else 503
    return HTTPException(status_code=status, detail=msg)


@router.get("/{sinistro_id}", response_model=Sinistro)
def get_sinistro(sinistro_id: str, token: str = Depends(verify_token)):
    try:
        return consultar_sinistro(sinistro_id)
    except ValueError as e:
        raise _tratar_erro(e) from e


@router.post("", response_model=Sinistro)
def post_sinistro(body: AberturaSinistroRequest, token: str = Depends(verify_token)):
    try:
        return abrir_sinistro(body.numero_apolice, body.tipo, body.descricao)
    except ValueError as e:
        raise _tratar_erro(e) from e
