"use client";

import { useEffect, useState } from "react";
import { API } from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState<string>("loading");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    API.getHealth()
      .then((data) => {
        setStatus(data.status);
      })
      .catch((err) => {
        setError(err.message);
        setStatus("error");
      });
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center">
      <div className="rounded-xl border p-6">
        <h1 className="text-2xl font-bold">Sklad Zero</h1>

        <p className="mt-4">
          API status:{" "}
          <span className="font-mono">{error ? error : status}</span>
        </p>
      </div>
    </main>
  );
}
