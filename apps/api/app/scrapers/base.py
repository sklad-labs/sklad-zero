from abc import ABC, abstractmethod

from app.schemas.anime import AnimeSearchResult


class AnimeScraper(ABC):
    @abstractmethod
    async def search(self, query: str) -> list[AnimeSearchResult]:
        pass