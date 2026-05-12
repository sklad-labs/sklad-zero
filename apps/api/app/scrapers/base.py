from abc import ABC, abstractmethod

from app.schemas.anime import AnimeEpisode, AnimeSearchResult, AnimeStreamSource


class AnimeScraper(ABC):
    @abstractmethod
    async def search(self, query: str) -> list[AnimeSearchResult]:
        pass

    @abstractmethod
    async def get_episodes(self, anime_id: str, translation_type: str = "sub") -> list[AnimeEpisode]:
        pass
    @abstractmethod
    async def get_streams(
        self,
        anime_id: str,
        episode_number: str,
        translation_type: str = "sub",
    ) -> list[AnimeStreamSource]:
        pass