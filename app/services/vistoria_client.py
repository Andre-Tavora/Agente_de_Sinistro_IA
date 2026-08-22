from app.schemas import Vistoria
from app.mock_data import VISTORIAS, SINISTROS


def consultar_vistoria(vistoria_id: str) -> Vistoria:
    dados = VISTORIAS.get(vistoria_id)
    if not dados:
        raise ValueError(f"Vistoria {vistoria_id} não encontrada")
    return Vistoria(**dados)


def agendar_vistoria(sinistro_id: str, data_agendada: str, endereco: str) -> Vistoria:
    if sinistro_id not in SINISTROS:
        raise ValueError(f"Sinistro {sinistro_id} não encontrado")

    novo_id = f"VT{len(VISTORIAS) + 1:03d}"
    nova_vistoria = {
        "id": novo_id,
        "sinistro_id": sinistro_id,
        "data_agendada": data_agendada,
        "endereco": endereco,
        "status": "agendada",
    }
    VISTORIAS[novo_id] = nova_vistoria
    return Vistoria(**nova_vistoria)
