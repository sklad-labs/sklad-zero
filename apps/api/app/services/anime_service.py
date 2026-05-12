import httpx
from fastapi import HTTPException

from app.schemas.anime import AnimeEpisode, AnimeSearchResult
from app.scrapers.allanime import AllAnimeScraper

scraper = AllAnimeScraper()


async def search_anime(query: str) -> list[AnimeSearchResult]:
    try:
        return await scraper.search(query)
    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail="Anime source returned an error",
        ) from error
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail="Anime source is unavailable",
        ) from error
async def get_anime_episodes(
    anime_id: str,
    translation_type: str = "sub",
) -> list[AnimeEpisode]:
    try:
        return await scraper.get_episodes(anime_id, translation_type)
    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail="Anime source returned an error",
        ) from error
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail="Anime source is unavailable",
        ) from error