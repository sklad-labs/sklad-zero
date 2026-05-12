from fastapi import APIRouter, Query

from app.schemas.anime import AnimeEpisode, AnimeStreamSource
from app.services.anime_service import get_anime_episodes, get_episode_streams

router = APIRouter(prefix="/anime", tags=["anime"])


@router.get("/{anime_id}/episodes", response_model=list[AnimeEpisode])
async def get_episodes(
    anime_id: str,
    translation_type: str = Query("sub", pattern="^(sub|dub)$"),
):
    return await get_anime_episodes(anime_id, translation_type)

@router.get(
    "/{anime_id}/episodes/{episode_number}/stream",
    response_model=list[AnimeStreamSource],
)
async def get_streams(
    anime_id: str,
    episode_number: str,
    translation_type: str = Query("sub", pattern="^(sub|dub)$"),
):
    return await get_episode_streams(
        anime_id=anime_id,
        episode_number=episode_number,
        translation_type=translation_type,
    )