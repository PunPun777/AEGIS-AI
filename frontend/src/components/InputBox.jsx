import React from "react";

const InputBox = ({ value, onChange, onSubmit, loading, error }) => {
  return (
    <div className="input-section">
      <label htmlFor="geo-text" className="input-label">
        Geopolitical Intelligence Input
      </label>

      <textarea
        id="geo-text"
        className={`input-textarea ${error ? "input-textarea--error" : ""}`}
        placeholder="Paste or type a news article, intelligence report, or geopolitical summary…"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={8}
        spellCheck="false"
        disabled={loading}
      />

      {error && (
        <p className="input-error" role="alert">
          <span className="input-error__icon">⚠</span> {error}
        </p>
      )}

      <button
        id="analyse-btn"
        className={`analyse-btn ${loading ? "analyse-btn--loading" : ""}`}
        onClick={onSubmit}
        disabled={loading}
      >
        {loading ? (
          <>
            <span className="spinner" aria-hidden="true" />
            Analysing…
          </>
        ) : (
          <>
            <span className="btn-icon" aria-hidden="true">
              ⚡
            </span>
            Analyse
          </>
        )}
      </button>
    </div>
  );
};

export default InputBox;
