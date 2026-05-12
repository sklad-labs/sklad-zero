from app.schemas.anime import AnimeSearchResult

async def search_anime(query: str) -> list[AnimeSearchResult]:
    return [
        AnimeSearchResult(
            id=query.lower().replace(" ", "-"),
            title=f"{query}",
            image=None,
            year=None,
        ),
    ]