"use client";

import { useState } from "react";
import { API, AnimeSearchResult } from "@/lib/api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<AnimeSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await API.searchAnime(query);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-8">
      <section className="mx-auto max-w-2xl">
        <h1 className="text-3xl font-bold">Sklad Zero</h1>
        <p className="mt-2 text-gray-500">Search anime from the backend API.</p>

        <form onSubmit={handleSearch} className="mt-6 flex gap-2">
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search anime..."
            className="flex-1 rounded-lg border px-4 py-2"
          />

          <button
            type="submit"
            disabled={loading}
            className="rounded-lg border px-4 py-2"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        {error && <p className="mt-4 text-red-500">{error}</p>}

        <div className="mt-6 space-y-3">
          {results.map((anime) => (
            <div key={anime.id} className="rounded-lg border p-4">
              <h2 className="font-semibold">{anime.title}</h2>

              {anime.year && (
                <p className="text-sm text-gray-500">Year: {anime.year}</p>
              )}
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
