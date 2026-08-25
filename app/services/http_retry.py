import logging
import time
from typing import Callable, TypeVar

import httpx

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ExternalServiceError(Exception):
    """Erro definitivo após esgotar tentativas ou erro 4xx do serviço externo."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


def call_with_retry(
    request_fn: Callable[[], httpx.Response],
    service_name: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> dict:
    last_exception: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            response = request_fn()
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status < 500:
                logger.warning(f"[{service_name}] Erro de cliente ({status}). Sem retry.")
                raise ExternalServiceError(
                    f"Requisição inválida ao {service_name}: {status}",
                    status_code=status,
                ) from e

            last_exception = e
            _wait_before_retry(attempt, max_retries, base_delay, service_name, e)

        except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as e:
            last_exception = e
            _wait_before_retry(attempt, max_retries, base_delay, service_name, e)

    logger.error(f"[{service_name}] Falha definitiva após {max_retries} tentativas.")
    raise ExternalServiceError(
        f"{service_name} indisponível após múltiplas tentativas",
        status_code=getattr(getattr(last_exception, "response", None), "status_code", None),
    ) from last_exception


def _wait_before_retry(attempt, max_retries, base_delay, service_name, error):
    if attempt == max_retries:
        return
    delay = base_delay * (2 ** (attempt - 1))
    logger.warning(
        f"[{service_name}] Tentativa {attempt}/{max_retries} falhou: {error}. Retry em {delay:.1f}s."
    )
    time.sleep(delay)
