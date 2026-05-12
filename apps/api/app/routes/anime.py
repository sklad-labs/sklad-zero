from fastapi import APIRouter, Query

from app.schemas.anime import AnimeEpisode
from app.services.anime_service import get_anime_episodes

router = APIRouter(prefix="/anime", tags=["anime"])


@router.get("/{anime_id}/episodes", response_model=list[AnimeEpisode])
async def get_episodes(
    anime_id: str,
    translation_type: str = Query("sub", pattern="^(sub|dub)$"),
):
    return await get_anime_episodes(anime_id, translation_type)