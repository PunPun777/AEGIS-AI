import React, { useState } from "react";
import InputBox from "./components/InputBox";
import ResultCard from "./components/ResultCard";
import { analyseText } from "./services/api";
import "./styles/App.css";

const App = () => {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyse = async () => {
    // --- Validation ---
    if (!text.trim()) {
      setError("Please enter some text before analysing.");
      return;
    }

    setError("");
    setPrediction(null);
    setLoading(true);

    try {
      const data = await analyseText(text.trim());
      setPrediction(data.prediction);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Unable to reach the AEGIS-AI backend. Ensure the server is running on port 8000.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="app-header">
        <div className="app-header__inner">
          <div className="header-logo" aria-hidden="true">🛡</div>
          <div>
            <div className="header-title">AEGIS-AI</div>
            <div className="header-sub">Intelligence Interface · v1.0</div>
          </div>
          <div className="header-status">
            <span className="status-dot" />
            System Online
          </div>
        </div>
      </header>

      {/* ── Main ── */}
      <main className="app-main">
        {/* Hero */}
        <section className="hero" aria-labelledby="hero-title">
          <p className="hero__eyebrow">Geopolitical Risk Classification</p>
          <h1 id="hero-title" className="hero__title">
            AEGIS-AI Intelligence Interface
          </h1>
          <p className="hero__sub">
            Submit geopolitical text for real-time threat classification.
            Powered by a fine-tuned NLP model.
          </p>
        </section>

        {/* Input card */}
        <section className="card" aria-label="Text input">
          <InputBox
            value={text}
            onChange={setText}
            onSubmit={handleAnalyse}
            loading={loading}
            error={error}
          />
        </section>

        {/* Result */}
        {prediction && (
          <section aria-label="Analysis result">
            <ResultCard prediction={prediction} />
          </section>
        )}
      </main>

      {/* ── Footer ── */}
      <footer className="app-footer">
        AEGIS-AI · Geopolitical Intelligence Platform · {new Date().getFullYear()}
      </footer>
    </div>
  );
};

export default App;
