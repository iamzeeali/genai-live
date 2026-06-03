import { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!query.trim()) return;
    setLoading(true);
    const res = await fetch("http://localhost:8000/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResults(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "60px auto", fontFamily: "sans-serif" }}>
      <h1>🎬 Semantic Movie Search</h1>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && search()}
          placeholder="e.g. space adventure, love story, crime..."
          style={{ flex: 1, padding: 10, fontSize: 16 }}
        />
        <button onClick={search} style={{ padding: "10px 20px", fontSize: 16 }}>
          Search
        </button>
      </div>

      {loading && <p>Searching...</p>}

      <ul style={{ marginTop: 24, listStyle: "none", padding: 0 }}>
        {results.map((r) => (
          <li key={r.title} style={{ marginBottom: 16, borderBottom: "1px solid #eee", paddingBottom: 16 }}>
            <strong>{r.title}</strong>
            <span style={{ marginLeft: 8, color: "#888", fontSize: 13 }}>
              score: {r.score}
            </span>
            <p style={{ margin: "4px 0 0", color: "#444" }}>{r.summary}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}