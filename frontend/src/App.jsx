import React from "react";
import MainInterface from "./components/MainInterface";
import "./styles/App.css";

const App = () => {
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

        {/* Main Interface */}
        <MainInterface />
      </main>

      {/* ── Footer ── */}
      <footer className="app-footer">
        AEGIS-AI · Geopolitical Intelligence Platform · {new Date().getFullYear()}
      </footer>
    </div>
  );
};

export default App;
