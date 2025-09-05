from enum import StrEnum
from typing import Any, Literal

import httpx


class OpenData511Agency(StrEnum):
    SFMTA = "SF"


class OpenData511Client:
    def __init__(self, api_token: str) -> None:
        self._client = httpx.Client(
            base_url="https://api.511.org", params={"api_key": api_token}
        )

    def _authenticated_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_payload: dict[str, Any] | None = None,
    ) -> httpx.Response:
        response = self._client.request(method, path, params=params, json=json_payload)
        if response.status_code == 401:
            raise httpx.HTTPStatusError(
                "401 Unauthorized: OpenData511 api key is missing or invalid",
                request=response.request,
                response=response,
            )
        else:
            response.raise_for_status()
        return response

    def get_transit_stop_monitoring(
        self,
        agency: str,
        stopcode: str | int | None = None,
        format: Literal["json", "xml"] = "json",
    ):
        return self._authenticated_request(
            "get",
            "/transit/StopMonitoring",
            params={
                "agency": agency,
                "stopcode": stopcode,
                "format": format,
            },
        )
