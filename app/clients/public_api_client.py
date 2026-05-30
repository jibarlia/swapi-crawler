from typing import Any

import httpx

SWAPI_BASE_URL = "https://swapi.info/api"


class SWAPIClient:
    def __init__(self, base_url: str = SWAPI_BASE_URL, timeout: float = 30.0):
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

    def _fetch_all(self, path: str) -> list[dict[str, Any]]:
        response = self._client.get(path)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else data.get("results", data)

    def fetch_all_people(self) -> list[dict[str, Any]]:
        return self._fetch_all("/people")

    def fetch_all_films(self) -> list[dict[str, Any]]:
        return self._fetch_all("/films")

    def fetch_all_planets(self) -> list[dict[str, Any]]:
        return self._fetch_all("/planets")

    def fetch_all_species(self) -> list[dict[str, Any]]:
        return self._fetch_all("/species")

    def fetch_all_vehicles(self) -> list[dict[str, Any]]:
        return self._fetch_all("/vehicles")

    def fetch_all_starships(self) -> list[dict[str, Any]]:
        return self._fetch_all("/starships")

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
