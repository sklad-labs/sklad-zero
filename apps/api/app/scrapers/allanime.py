import httpx

from app.schemas.anime import AnimeSearchResult
from app.scrapers.base import AnimeScraper


class AllAnimeScraper(AnimeScraper):
    def __init__(self) -> None:
        self.api_url = "https://api.allanime.day/api"
        self.referer = "https://allmanga.to"

        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": self.referer,
            "Content-Type": "application/json",
        }

        self.search_gql = """
        query(
          $search: SearchInput
          $limit: Int
          $page: Int
          $translationType: VaildTranslationTypeEnumType
          $countryOrigin: VaildCountryOriginEnumType
        ) {
          shows(
            search: $search
            limit: $limit
            page: $page
            translationType: $translationType
            countryOrigin: $countryOrigin
          ) {
            edges {
              _id
              name
              availableEpisodes
              __typename
            }
          }
        }
        """

    async def search(self, query: str) -> list[AnimeSearchResult]:
        payload = {
            "variables": {
                "search": {
                    "allowAdult": False,
                    "allowUnknown": False,
                    "query": query,
                },
                "limit": 40,
                "page": 1,
                "translationType": "sub",
                "countryOrigin": "ALL",
            },
            "query": self.search_gql,
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=15) as client:
            response = await client.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()

        return self._parse_search_response(data)

    def _parse_search_response(self, data: dict) -> list[AnimeSearchResult]:
        edges = data.get("data", {}).get("shows", {}).get("edges", [])

        results: list[AnimeSearchResult] = []

        for item in edges:
            anime_id = item.get("_id")
            title = item.get("name")

            if not anime_id or not title:
                continue

            results.append(
                AnimeSearchResult(
                    id=anime_id,
                    title=title,
                    image=None,
                    year=None,
                )
            )

        return results