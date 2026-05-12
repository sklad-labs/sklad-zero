from pydantic import BaseModel

class AnimeSearchResult(BaseModel):
    id: str
    title: str
    image: str | None = None
    year: int | None = None

class AnimeEpisode(BaseModel):
    number: str


class AnimeStreamSource(BaseModel):
    url: str
    quality: str | None = None
    source: str | None = None
    type: str | None = None