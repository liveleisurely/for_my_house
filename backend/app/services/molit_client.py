from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from app.core.config import Settings


@dataclass(frozen=True)
class MolitEndpoint:
    name: str
    url: str
    trade_type: str


MOLIT_ENDPOINTS: dict[str, MolitEndpoint] = {
    "pre_sale_right": MolitEndpoint(
        name="아파트 분양권전매 실거래",
        url="https://apis.data.go.kr/1613000/RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade",
        trade_type="pre_sale_right",
    ),
}


class MolitClient:
    """Thin client for MOLIT OpenAPI.

    XML parsing is intentionally left outside this class so transport failure handling and payload
    normalization can be tested independently.
    """

    def __init__(self, settings: Settings):
        self._settings = settings

    async def fetch(self, endpoint_key: str, legal_dong_code_5: str, year_month: str) -> str:
        if self._settings.molit_service_key is None:
            raise RuntimeError("MOLIT_SERVICE_KEY is required to fetch public transaction data")
        endpoint = MOLIT_ENDPOINTS[endpoint_key]
        params: dict[str, Any] = {
            "serviceKey": self._settings.molit_service_key,
            "LAWD_CD": legal_dong_code_5,
            "DEAL_YMD": year_month,
        }
        url = f"{endpoint.url}?{urlencode(params)}"
        async with httpx.AsyncClient(timeout=self._settings.request_timeout_seconds) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
