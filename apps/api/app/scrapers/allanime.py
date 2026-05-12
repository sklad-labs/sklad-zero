import base64
import hashlib
import json

import httpx
from Crypto.Cipher import AES

from app.schemas.anime import AnimeEpisode, AnimeSearchResult, AnimeStreamSource
from app.scrapers.base import AnimeScraper

_BLOCKED_SOURCE_NAMES = {"Vid-mp4"}


class AllAnimeScraper(AnimeScraper):
    def __init__(self) -> None:
        self.api_url = "https://api.allanime.day/api"
        self.referer = "https://allmanga.to"

        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": self.referer,
            "Content-Type": "application/json",
        }

        self.episode_query_hash = (
            "d405d0edd690624b66baba3068e0edc3ac90f1597d898a1ec8db4e5c43c00fec"
        )

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

        self.episodes_list_gql = """
        query($showId: String!) {
          show(_id: $showId) {
            _id
            availableEpisodes
          }
        }
        """

        self.episode_embed_gql = """
        query(
          $showId: String!
          $translationType: VaildTranslationTypeEnumType!
          $episodeString: String!
        ) {
          episode(
            showId: $showId
            translationType: $translationType
            episodeString: $episodeString
          ) {
            episodeString
            sourceUrls
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

    async def get_episodes(
        self,
        anime_id: str,
        translation_type: str = "sub",
    ) -> list[AnimeEpisode]:
        payload = {
            "variables": {
                "showId": anime_id,
            },
            "query": self.episodes_list_gql,
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=15) as client:
            response = await client.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()

        show = data.get("data", {}).get("show") or {}
        available = show.get("availableEpisodes", {}).get(translation_type, [])

        if isinstance(available, int):
            episode_numbers = range(1, available + 1)
        elif isinstance(available, list):
            episode_numbers = available
        else:
            episode_numbers = []

        return [AnimeEpisode(number=str(episode)) for episode in episode_numbers]

    async def get_streams(
        self,
        anime_id: str,
        episode_number: str,
        translation_type: str = "sub",
    ) -> list[AnimeStreamSource]:
        variables = {
            "showId": anime_id,
            "translationType": translation_type,
            "episodeString": episode_number,
        }

        extensions = {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": self.episode_query_hash,
            }
        }

        persisted_headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://youtu-chan.com",
            "Origin": "https://youtu-chan.com",
        }

        params = {
            "variables": json.dumps(variables, separators=(",", ":")),
            "extensions": json.dumps(extensions, separators=(",", ":")),
        }

        async with httpx.AsyncClient(headers=persisted_headers, timeout=15) as client:
            response = await client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()

        tobeparsed = data.get("data", {}).get("tobeparsed")
        if tobeparsed:
            return self._parse_stream_response({"data": self._decrypt_tobeparsed(tobeparsed)})

        if self._has_stream_data(data):
            return self._parse_stream_response(data)

        return []

    def _parse_search_response(self, data: dict) -> list[AnimeSearchResult]:
        edges = data.get("data", {}).get("shows", {}).get("edges", [])

        results: list[AnimeSearchResult] = []

        for item in edges:
            if not isinstance(item, dict):
                continue

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

    def _parse_stream_response(self, data: dict) -> list[AnimeStreamSource]:
        episode = data.get("data", {}).get("episode")

        if not episode:
            return []

        source_urls = episode.get("sourceUrls") or []

        results: list[AnimeStreamSource] = []

        for source in source_urls:
            if not isinstance(source, dict):
                continue

            source_url = source.get("sourceUrl")
            source_name = source.get("sourceName")

            if not source_url or source_name in _BLOCKED_SOURCE_NAMES:
                continue

            if source_url.startswith("--"):
                source_url = self._decode_xor_url(source_url[2:])

            if source_url.startswith("/"):
                continue

            results.append(
                AnimeStreamSource(
                    url=source_url,
                    source=source_name,
                    quality=None,
                    type=None,
                )
            )

        return results

    def _decrypt_tobeparsed(self, tobeparsed: str) -> dict:
        padding = (4 - len(tobeparsed) % 4) % 4
        raw = base64.b64decode(tobeparsed + "=" * padding)
        key = hashlib.sha256(b"Xot36i3lK3:v1").digest()
        nonce = raw[1:13]
        ctr_iv = bytes.fromhex(nonce.hex() + "00000002")
        ct_len = len(raw) - 13 - 16
        plaintext = AES.new(key, AES.MODE_CTR, initial_value=ctr_iv, nonce=b"").decrypt(raw[13 : 13 + ct_len])
        return json.loads(plaintext)

    def _decode_xor_url(self, hex_str: str) -> str:
        return bytes([int(hex_str[i : i + 2], 16) ^ 56 for i in range(0, len(hex_str), 2)]).decode("utf-8", errors="ignore")

    def _has_stream_data(self, data: dict) -> bool:
        episode = data.get("data", {}).get("episode")

        if not episode:
            return False

        source_urls = episode.get("sourceUrls")

        return isinstance(source_urls, list) and len(source_urls) > 0