import httpx
from fastapi import HTTPException

from app.schemas.anime import AnimeEpisode, AnimeSearchResult, AnimeStreamSource
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

async def get_episode_streams(
    anime_id: str,
    episode_number: str,
    translation_type: str = "sub",
) -> list[AnimeStreamSource]:
    try:
        return await scraper.get_streams(
            anime_id=anime_id,
            episode_number=episode_number,
            translation_type=translation_type,
        )
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