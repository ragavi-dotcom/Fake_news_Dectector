import { useState } from "react";
import { predictArticle } from "./api.js";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await predictArticle(text));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function onClear() {
    setText("");
    setResult(null);
    setError("");
  }

  return (
    <main className="page">
      <h1>Fake News Detector</h1>
      <p className="sub">Paste an article and get an instant read.</p>

      <form onSubmit={onSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste the article here…"
          rows={10}
          required
          minLength={20}
        />
        <div className="row">
          <button type="submit" disabled={loading || text.length < 20}>
            {loading ? "Checking…" : "Check article"}
          </button>
          <button type="button" className="ghost" onClick={onClear} disabled={loading || (!text && !result && !error)}>
            Clear
          </button>
        </div>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <section key={result.confidence} className={`result ${result.label}`}>
          <strong>{result.label === "fake" ? "Likely fake" : "Likely real"}</strong>
          <div className="bar">
            <div className="fill" style={{ width: `${result.confidence * 100}%` }} />
          </div>
          <span className="pct">{(result.confidence * 100).toFixed(0)}% confidence</span>

          {result.words?.length > 0 && (
            <div className="chips">
              {result.words.map((w) => (
                <span key={w.word} className={w.weight >= 0 ? "real" : "fake"}>{w.word}</span>
              ))}
            </div>
          )}
        </section>
      )}
    </main>
  );
}