import os

import httpx

from app.schemas import Vistoria
from app.services.http_retry import call_with_retry, ExternalServiceError

MOCK_API_URL = os.getenv("MOCK_API_URL", "http://localhost:8001")


def consultar_vistoria(vistoria_id: str) -> Vistoria:
    try:
        dados = call_with_retry(
            request_fn=lambda: httpx.get(
                f"{MOCK_API_URL}/vistorias/{vistoria_id}", timeout=5.0
            ),
            service_name="vistoria_client",
        )
    except ExternalServiceError as e:
        if e.status_code == 404:
            raise ValueError(f"Vistoria {vistoria_id} não encontrada") from e
        raise ValueError(
            "Serviço de vistorias indisponível no momento, tente novamente em breve"
        ) from e

    return Vistoria(**dados)


def agendar_vistoria(sinistro_id: str, data_agendada: str, endereco: str) -> Vistoria:
    try:
        dados = call_with_retry(
            request_fn=lambda: httpx.post(
                f"{MOCK_API_URL}/vistorias",
                json={
                    "sinistro_id": sinistro_id,
                    "data_agendada": data_agendada,
                    "endereco": endereco,
                },
                timeout=5.0,
            ),
            service_name="vistoria_client",
        )
    except ExternalServiceError as e:
        if e.status_code == 404:
            raise ValueError(f"Sinistro {sinistro_id} não encontrado") from e
        raise ValueError(
            "Serviço de vistorias indisponível no momento, tente novamente em breve"
        ) from e

    return Vistoria(**dados)
