import logging
from unittest.mock import MagicMock

import httpx
import pytest

from app.services.http_retry import call_with_retry, ExternalServiceError


def test_retry_on_connect_error_then_success(caplog):
    """
    Simula serviço fora do ar em 2 tentativas (ConnectError) e sucesso na 3ª.
    Evidencia backoff exponencial nos logs.
    """
    resp_ok = MagicMock(spec=httpx.Response)
    resp_ok.raise_for_status.return_value = None
    resp_ok.json.return_value = {"numero_apolice": "AP001", "segurado": "Carlos"}

    call_count = {"n": 0}

    def request_fn():
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise httpx.ConnectError("Connection refused", request=MagicMock())
        return resp_ok

    with caplog.at_level(logging.WARNING):
        result = call_with_retry(request_fn, service_name="apolice_client", base_delay=0.1)

    assert result == {"numero_apolice": "AP001", "segurado": "Carlos"}
    assert call_count["n"] == 3
    assert "Tentativa 1/3 falhou" in caplog.text
    assert "Retry em" in caplog.text


def test_connect_error_exhausted_raises_external_service_error(caplog):
    """
    Serviço fora do ar nas 3 tentativas. Deve esgotar e levantar
    ExternalServiceError, sem deixar ConnectError escapar sem tratamento.
    """
    def request_fn():
        raise httpx.ConnectError("Connection refused", request=MagicMock())

    with caplog.at_level(logging.WARNING):
        with pytest.raises(ExternalServiceError) as exc_info:
            call_with_retry(request_fn, service_name="apolice_client", base_delay=0.1)

    assert "indisponível após múltiplas tentativas" in str(exc_info.value)
    assert "Falha definitiva após 3 tentativas" in caplog.text


def test_client_error_4xx_no_retry(caplog):
    """
    Erro 4xx não deve disparar retry: request_fn é chamada só 1 vez.
    """
    resp_404 = MagicMock(spec=httpx.Response)
    resp_404.status_code = 404
    error = httpx.HTTPStatusError("Not Found", request=MagicMock(), response=resp_404)

    call_count = {"n": 0}

    def request_fn():
        call_count["n"] += 1
        raise error

    with caplog.at_level(logging.WARNING):
        with pytest.raises(ExternalServiceError) as exc_info:
            call_with_retry(request_fn, service_name="apolice_client", base_delay=0.1)

    assert call_count["n"] == 1
    assert exc_info.value.status_code == 404
    assert "Sem retry" in caplog.text
