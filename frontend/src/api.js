const API_BASE = "http://localhost:8000";

export async function predictArticle(text) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();  // { label: "fake"|"real", confidence: number }
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
