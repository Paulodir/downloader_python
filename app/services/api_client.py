from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from app.core.config import Config
from app.core.exceptions import ApiClientError, ConfigurationError


class ApiClient:
    def __init__(self, config: Config):
        self.config = config

    def fetch_edital(self, codigo: str, tipo_documento: str) -> dict[str, Any]:
        if not self.config.api_base_url:
            raise ConfigurationError(
                "Defina APP_API_BASE_URL para habilitar a sincronizacao com a API HTTP."
            )

        endpoint = self.config.api_edital_path.format(codigo=codigo)
        params = {
            "codigo": codigo,
            "tipo_documento": tipo_documento,
        }

        try:
            with httpx.Client(
                base_url=self.config.api_base_url,
                timeout=self.config.request_timeout,
                headers={"Accept": "application/json"},
            ) as client:
                response = client.get(endpoint, params=params)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPStatusError as exc:
            raise ApiClientError(
                f"API retornou status {exc.response.status_code} para o edital {codigo}."
            ) from exc
        except httpx.HTTPError as exc:
            raise ApiClientError(f"Falha de comunicacao com a API: {exc}") from exc
        except ValueError as exc:
            raise ApiClientError("A API retornou um JSON invalido.") from exc

        if not isinstance(payload, Mapping):
            raise ApiClientError("A resposta da API precisa ser um objeto JSON.")

        return dict(payload)
