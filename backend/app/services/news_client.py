from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from app.core.config import Settings
from app.services.normalization import source_hash


class NaverNewsClient:
    def __init__(self, settings: Settings):
        self._settings = settings

    async def search(self, query: str, display: int = 10) -> list[dict[str, Any]]:
        if self._settings.naver_client_id is None or self._settings.naver_client_secret is None:
            raise RuntimeError("NAVER_CLIENT_ID and NAVER_CLIENT_SECRET are required")
        headers = {
            "X-Naver-Client-Id": self._settings.naver_client_id,
            "X-Naver-Client-Secret": self._settings.naver_client_secret,
        }
        params = {"query": query, "display": display, "sort": "date"}
        async with httpx.AsyncClient(timeout=self._settings.request_timeout_seconds) as client:
            response = await client.get(
                "https://openapi.naver.com/v1/search/news.json", headers=headers, params=params
            )
            response.raise_for_status()
            payload = response.json()
        return [self._normalize(query, item) for item in payload.get("items", [])]

    @staticmethod
    def _normalize(query: str, item: dict[str, Any]) -> dict[str, Any]:
        published_at: datetime | None = None
        if pub_date := item.get("pubDate"):
            published_at = parsedate_to_datetime(pub_date)
        url = item.get("originallink") or item.get("link")
        return {
            "provider": "naver",
            "title": _strip_html(item.get("title", "")),
            "url": url,
            "published_at": published_at,
            "snippet": _strip_html(item.get("description", "")),
            "query": query,
            "source_hash": source_hash(["naver", url]),
        }


def _strip_html(value: str) -> str:
    return value.replace("<b>", "").replace("</b>", "").replace("&quot;", '"')
