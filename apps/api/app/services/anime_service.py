from app.schemas.anime import AnimeSearchResult
from app.scrapers.mock import MockAnimeScraper

scraper = MockAnimeScraper()


async def search_anime(query: str) -> list[AnimeSearchResult]:
    return await scraper.search(query)