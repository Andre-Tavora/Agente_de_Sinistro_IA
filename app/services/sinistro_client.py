import os

import httpx

from app.schemas import Sinistro
from app.services.http_retry import call_with_retry, ExternalServiceError

MOCK_API_URL = os.getenv("MOCK_API_URL", "http://localhost:8001")


def consultar_sinistro(sinistro_id: str) -> Sinistro:
    try:
        dados = call_with_retry(
            request_fn=lambda: httpx.get(
                f"{MOCK_API_URL}/sinistros/{sinistro_id}", timeout=5.0
            ),
            service_name="sinistro_client",
        )
    except ExternalServiceError as e:
        if e.status_code == 404:
            raise ValueError(f"Sinistro {sinistro_id} não encontrado") from e
        raise ValueError(
            f"Serviço de sinistros indisponível no momento, tente novamente em breve"
        ) from e

    return Sinistro(**dados)


def abrir_sinistro(numero_apolice: str, tipo: str, descricao: str) -> Sinistro:
    try:
        dados = call_with_retry(
            request_fn=lambda: httpx.post(
                f"{MOCK_API_URL}/sinistros",
                json={
                    "numero_apolice": numero_apolice,
                    "tipo": tipo,
                    "descricao": descricao,
                },
                timeout=5.0,
            ),
            service_name="sinistro_client",
        )
    except ExternalServiceError as e:
        if e.status_code == 404:
            raise ValueError(f"Apólice {numero_apolice} não encontrada") from e
        raise ValueError(
            "Serviço de sinistros indisponível no momento, tente novamente em breve"
        ) from e

    return Sinistro(**dados)
