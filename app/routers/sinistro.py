from fastapi import APIRouter, Depends, HTTPException
from app.auth import verify_token
from app.schemas import Sinistro
from app.mock_data import SINISTROS

router = APIRouter(prefix="/sinistro", tags=["sinistro"])

@router.get("/{sinistro_id}", response_model=Sinistro)
def get_sinistro(sinistro_id: str, token: str = Depends(verify_token)):
    sinistro = SINISTROS.get(sinistro_id)
    if not sinistro:
        raise HTTPException(status_code=404, detail="Sinistro não encontrado")
    return sinistro