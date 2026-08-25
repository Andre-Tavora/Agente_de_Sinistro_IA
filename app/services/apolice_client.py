import os

import httpx

from app.schemas import Apolice
from app.services.http_retry import call_with_retry, ExternalServiceError

MOCK_API_URL = os.getenv("MOCK_API_URL", "http://localhost:8001")


def consultar_apolice(numero_apolice: str) -> Apolice:
    try:
        dados = call_with_retry(
            request_fn=lambda: httpx.get(
                f"{MOCK_API_URL}/apolices/{numero_apolice}", timeout=5.0
            ),
            service_name="apolice_client",
        )
    except ExternalServiceError as e:
        if e.status_code == 404:
            raise ValueError(f"Apólice {numero_apolice} não encontrada") from e
        raise ValueError(
            "Serviço de apólices indisponível no momento, tente novamente em breve"
        ) from e

    return Apolice(**dados)
