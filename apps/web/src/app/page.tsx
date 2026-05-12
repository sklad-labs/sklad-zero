"use client";

import type React from "react";
import { useState } from "react";
import { API, type AnimeEpisode, type AnimeSearchResult } from "@/lib/api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<AnimeSearchResult[]>([]);
  const [selectedAnime, setSelectedAnime] = useState<AnimeSearchResult | null>(
    null,
  );
  const [episodes, setEpisodes] = useState<AnimeEpisode[]>([]);

  const [searchLoading, setSearchLoading] = useState(false);
  const [episodesLoading, setEpisodesLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);

  async function handleSearch(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      return;
    }

    setSearchLoading(true);
    setError(null);
    setSelectedAnime(null);
    setEpisodes([]);

    try {
      const data = await API.searchAnime(trimmedQuery);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to search anime");
    } finally {
      setSearchLoading(false);
    }
  }

  async function handleSelectAnime(anime: AnimeSearchResult) {
    if (selectedAnime?.id === anime.id) {
      setSelectedAnime(null);
      setEpisodes([]);
      setEpisodesLoading(false);
      setError(null);
      return;
    }

    setSelectedAnime(anime);
    setEpisodes([]);
    setEpisodesLoading(true);
    setError(null);

    try {
      const data = await API.getEpisodes(anime.id);
      setEpisodes(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load episodes");
    } finally {
      setEpisodesLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 p-8 text-zinc-100">
      <section className="mx-auto max-w-3xl">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Sklad Zero</h1>
          <p className="mt-2 text-zinc-400">
            Search anime and load available episodes from the backend API.
          </p>
        </div>

        <form onSubmit={handleSearch} className="mt-6 flex gap-2">
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search anime..."
            className="flex-1 rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-2 text-zinc-100 placeholder:text-zinc-500 outline-none transition focus:border-zinc-400 focus:bg-zinc-950 focus:ring-2 focus:ring-zinc-700"
          />

          <button
            type="submit"
            disabled={searchLoading}
            className="rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-2 text-zinc-100 transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {searchLoading ? "Searching..." : "Search"}
          </button>
        </form>

        {error && (
          <div className="mt-4 rounded-lg border border-red-900/60 bg-red-950/40 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <div className="mt-6 grid gap-3">
          {results.map((anime) => {
            const isSelected = selectedAnime?.id === anime.id;

            return (
              <div key={anime.id} className="grid gap-3">
                <button
                  type="button"
                  onClick={() => handleSelectAnime(anime)}
                  className={`rounded-lg border p-4 text-left transition ${
                    isSelected
                      ? "border-zinc-300 bg-zinc-800"
                      : "border-zinc-800 bg-zinc-900 hover:border-zinc-600 hover:bg-zinc-800"
                  }`}
                >
                  <div className="flex items-center justify-between gap-4">
                    <h2 className="font-semibold text-zinc-100">
                      {anime.title}
                    </h2>

                    <span className="shrink-0 rounded-full border border-zinc-700 px-2 py-1 text-xs text-zinc-400">
                      {isSelected ? "Hide" : "Open"}
                    </span>
                  </div>

                  <p className="mt-1 text-xs text-zinc-500">ID: {anime.id}</p>

                  {anime.year && (
                    <p className="mt-1 text-sm text-zinc-400">
                      Year: {anime.year}
                    </p>
                  )}
                </button>

                {isSelected && (
                  <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
                    <div>
                      <h3 className="text-xl font-bold text-zinc-100">
                        {selectedAnime.title}
                      </h3>
                      <p className="mt-1 text-sm text-zinc-400">
                        Available episodes
                      </p>
                    </div>

                    {episodesLoading && (
                      <p className="mt-4 text-sm text-zinc-400">
                        Loading episodes...
                      </p>
                    )}

                    {!episodesLoading && episodes.length === 0 && (
                      <p className="mt-4 text-sm text-zinc-400">
                        No episodes found.
                      </p>
                    )}

                    {episodes.length > 0 && (
                      <div className="mt-4 grid grid-cols-4 gap-2 sm:grid-cols-6 md:grid-cols-8">
                        {episodes.map((episode) => (
                          <button
                            key={episode.number}
                            type="button"
                            className="rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm text-zinc-100 transition hover:border-zinc-500 hover:bg-zinc-800"
                          >
                            {episode.number}
                          </button>
                        ))}
                      </div>
                    )}
                  </section>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}
