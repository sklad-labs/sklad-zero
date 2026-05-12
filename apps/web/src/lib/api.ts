const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type AnimeSearchResult = {
  id: string;
  title: string;
  image: string | null;
  year: number | null;
};

export type AnimeEpisode = {
  number: string;
};

export const API = {
  getHealth: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error("Failed to fetch health");
    }

    return response.json();
  },

  searchAnime: async (query: string): Promise<AnimeSearchResult[]> => {
    const params = new URLSearchParams({ q: query });

    const response = await fetch(`${API_BASE_URL}/search?${params.toString()}`);

    if (!response.ok) {
      throw new Error("Failed to search anime");
    }

    return response.json();
  },
  getEpisodes: async (
    animeId: string,
    translationType: "sub" | "dub" = "sub",
  ): Promise<AnimeEpisode[]> => {
    const params = new URLSearchParams({ translation_type: translationType });

    const response = await fetch(
      `${API_BASE_URL}/anime/${animeId}/episodes?${params.toString()}`,
    );

    if (!response.ok) {
      throw new Error("Failed to fetch episodes");
    }

    return response.json();
  },
};
