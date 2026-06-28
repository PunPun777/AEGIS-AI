import React, { useState } from "react";

const HybridDecisionPanel = ({ 
  overridden, 
  originalPrediction, 
  reason, 
  categories, 
  keywords 
}) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!overridden) return null;

  return (
    <div className="explanation-panel hybrid-panel">
      <button 
        className="explanation-toggle hybrid-toggle" 
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span className="explanation-toggle-text">Hybrid Override Details</span>
        <span className="explanation-toggle-icon">{isOpen ? "▲" : "▼"}</span>
      </button>
      
      <div className={`explanation-content ${isOpen ? 'is-open' : ''}`}>
        <div className="explanation-content-inner hybrid-content-inner">
          <p className="hybrid-reason">{reason}</p>
          
          <div className="hybrid-details">
            <div className="hybrid-detail-group">
              <strong>Original ML Prediction:</strong>
              <span className={`hybrid-badge hybrid-badge--${originalPrediction?.toLowerCase()}`}>
                {originalPrediction?.toUpperCase()}
              </span>
            </div>
            
            {categories && categories.length > 0 && (
              <div className="hybrid-detail-group">
                <strong>Matched Categories:</strong>
                <div className="hybrid-tags">
                  {categories.map((cat, idx) => (
                    <span key={idx} className="hybrid-tag cat-tag">{cat}</span>
                  ))}
                </div>
              </div>
            )}
            
            {keywords && keywords.length > 0 && (
              <div className="hybrid-detail-group">
                <strong>Matched Keywords:</strong>
                <div className="hybrid-tags">
                  {keywords.map((kw, idx) => (
                    <span key={idx} className="hybrid-tag kw-tag">{kw}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HybridDecisionPanel;
