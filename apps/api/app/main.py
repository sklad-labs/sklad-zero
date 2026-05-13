import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.anime import router as anime_router
from app.routes.search import router as search_router


def get_cors_origins() -> list[str]:
    raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")

    return [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Sklad Zero API",
    description="API for Sklad Zero application",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(search_router)
app.include_router(anime_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}