import React, { useState } from "react";

const DiagnosticsPanel = ({ diagnostics }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!diagnostics) return null;

  const {
    ml_prediction,
    ml_confidence,
    ml_evidence_score,
    matched_keywords,
    matched_categories,
    category_scores,
    dominant_category,
    domain_evidence_score,
    override_applied,
    override_reason,
    final_prediction,
    decision,
  } = diagnostics;

  return (
    <div className="explanation-panel diagnostics-panel">
      <button 
        className="explanation-toggle diagnostics-toggle" 
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span className="explanation-toggle-text">Developer Diagnostics</span>
        <span className="explanation-toggle-icon">{isOpen ? "▲" : "▼"}</span>
      </button>
      
      <div className={`explanation-content ${isOpen ? 'is-open' : ''}`}>
        <div className="explanation-content-inner diagnostics-content-inner">
          <div className="diagnostics-grid">
            <div className="diagnostic-item">
              <span className="diagnostic-label">ML Prediction</span>
              <span className="diagnostic-value">{ml_prediction}</span>
            </div>
            <div className="diagnostic-item">
              <span className="diagnostic-label">Final Prediction</span>
              <span className="diagnostic-value">{final_prediction}</span>
            </div>
            <div className="diagnostic-item">
              <span className="diagnostic-label">Confidence</span>
              <span className="diagnostic-value">{(ml_confidence * 100).toFixed(2)}%</span>
            </div>
            <div className="diagnostic-item">
              <span className="diagnostic-label">ML Evidence</span>
              <span className="diagnostic-value">{ml_evidence_score?.toFixed(4)}</span>
            </div>
            <div className="diagnostic-item">
              <span className="diagnostic-label">Domain Evidence</span>
              <span className="diagnostic-value">{domain_evidence_score?.toFixed(4)}</span>
            </div>
            <div className="diagnostic-item">
              <span className="diagnostic-label">Decision</span>
              <span className="diagnostic-value">{decision}</span>
            </div>
            <div className="diagnostic-item">
              <span className="diagnostic-label">Override</span>
              <span className="diagnostic-value">{override_applied ? "Yes" : "No"}</span>
            </div>
          </div>

          {override_reason && (
            <div className="diagnostic-section">
              <span className="diagnostic-label">Reason</span>
              <p className="diagnostic-reason">{override_reason}</p>
            </div>
          )}

          {dominant_category && (
            <div className="diagnostic-section">
              <span className="diagnostic-label">Dominant Category</span>
              <div>
                <span className="hybrid-tag cat-tag">{dominant_category}</span>
              </div>
            </div>
          )}

          {matched_categories?.length > 0 && (
            <div className="diagnostic-section">
              <span className="diagnostic-label">Matched Categories</span>
              <div className="hybrid-tags">
                {matched_categories.map((cat, idx) => (
                  <span key={idx} className="hybrid-tag cat-tag">
                    {cat} {category_scores?.[cat] !== undefined ? `(${category_scores[cat].toFixed(2)})` : ""}
                  </span>
                ))}
              </div>
            </div>
          )}

          {matched_keywords?.length > 0 && (
            <div className="diagnostic-section">
              <span className="diagnostic-label">Matched Keywords</span>
              <div className="hybrid-tags">
                {matched_keywords.map((kw, idx) => (
                  <span key={idx} className="hybrid-tag kw-tag">{kw}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiagnosticsPanel;
