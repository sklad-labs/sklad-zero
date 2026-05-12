from fastapi import APIRouter, Query

from app.schemas.anime import AnimeSearchResult
from app.services.anime_service import search_anime

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[AnimeSearchResult])
async def search(q: str = Query(..., description="Search query for anime titles")):
    return await search_anime(q)