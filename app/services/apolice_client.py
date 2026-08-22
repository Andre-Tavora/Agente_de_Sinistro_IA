from app.schemas import Apolice
from app.mock_data import APOLICES


def consultar_apolice(numero_apolice: str) -> Apolice:
    dados = APOLICES.get(numero_apolice)
    if not dados:
        raise ValueError(f"Apólice {numero_apolice} não encontrada")
    return Apolice(**dados)
