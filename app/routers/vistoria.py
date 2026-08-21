from fastapi import APIRouter, Depends, HTTPException
from app.auth import verify_token
from app.schemas import Vistoria
from app.mock_data import VISTORIAS

router = APIRouter(prefix="/vistoria", tags=["vistoria"])

@router.get("/{vistoria_id}", response_model=Vistoria)
def get_vistoria(vistoria_id: str, token: str = Depends(verify_token)):
    vistoria = VISTORIAS.get(vistoria_id)
    if not vistoria:
        raise HTTPException(status_code=404, detail="Vistoria não encontrada")
    return vistoria