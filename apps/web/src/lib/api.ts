const API_Base_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export const API = {
  getHealth: async () => {
    const response = await fetch(`${API_Base_URL}/health`);
    if (!response.ok) {
      throw new Error("Failed to fetch health");
    }
    return response.json();
  },
};
