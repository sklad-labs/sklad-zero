from pydantic import BaseModel

class AnimeSearchResult(BaseModel):
    id: str
    title: str
    image: str | None = None
    year: int | None = None

class AnimeEpisode(BaseModel):
    number: str