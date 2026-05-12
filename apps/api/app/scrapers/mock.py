from app.schemas.anime import AnimeSearchResult
from app.scrapers.base import AnimeScraper


class MockAnimeScraper(AnimeScraper):
    async def search(self, query: str) -> list[AnimeSearchResult]:
        normalized_query = query.lower().replace(" ", "-")

        return [
            AnimeSearchResult(
                id=f"{normalized_query}-1",
                title=f"{query} Result 1",
                image=None,
                year=None,
            ),
            AnimeSearchResult(
                id=f"{normalized_query}-2",
                title=f"{query} Result 2",
                image=None,
                year=None,
            ),
        ]