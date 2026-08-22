from app.schemas import Sinistro
from app.mock_data import SINISTROS, APOLICES


def consultar_sinistro(sinistro_id: str) -> Sinistro:
    dados = SINISTROS.get(sinistro_id)
    if not dados:
        raise ValueError(f"Sinistro {sinistro_id} não encontrado")
    return Sinistro(**dados)


def abrir_sinistro(numero_apolice: str, tipo: str, descricao: str) -> Sinistro:
    if numero_apolice not in APOLICES:
        raise ValueError(f"Apólice {numero_apolice} não encontrada")

    novo_id = f"SN{len(SINISTROS) + 1:03d}"
    novo_sinistro = {
        "id": novo_id,
        "numero_apolice": numero_apolice,
        "tipo": tipo,
        "descricao": descricao,
        "status": "aberto",
    }
    SINISTROS[novo_id] = novo_sinistro
    return Sinistro(**novo_sinistro)
