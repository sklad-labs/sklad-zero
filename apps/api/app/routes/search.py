from fastapi import APIRouter, Query
from app.schemas.anime import AnimeSearchResult

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("", response_model=list[AnimeSearchResult])
async def search_anime(q: str = Query(..., description="Search query for anime titles")):
    return [
        AnimeSearchResult(
            id=q.lower().replace(" ", "-"),
            title=f"{q}",
            image=None,
            year=None,
        ),
    ]