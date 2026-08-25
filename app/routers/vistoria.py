from fastapi import APIRouter, Depends, HTTPException
from app.auth import verify_token
from app.schemas import Vistoria
from app.services.vistoria_client import consultar_vistoria, agendar_vistoria
from pydantic import BaseModel

router = APIRouter(prefix="/vistoria", tags=["vistoria"])


class AgendamentoVistoriaRequest(BaseModel):
    sinistro_id: str
    data_agendada: str
    endereco: str


def _tratar_erro(e: ValueError) -> HTTPException:
    msg = str(e)
    status = 404 if "não encontrada" in msg or "não encontrado" in msg else 503
    return HTTPException(status_code=status, detail=msg)


@router.get("/{vistoria_id}", response_model=Vistoria)
def get_vistoria(vistoria_id: str, token: str = Depends(verify_token)):
    try:
        return consultar_vistoria(vistoria_id)
    except ValueError as e:
        raise _tratar_erro(e) from e


@router.post("", response_model=Vistoria)
def post_vistoria(body: AgendamentoVistoriaRequest, token: str = Depends(verify_token)):
    try:
        return agendar_vistoria(body.sinistro_id, body.data_agendada, body.endereco)
    except ValueError as e:
        raise _tratar_erro(e) from e
