import React, { useState } from "react";
import ExplanationList from "./ExplanationList";

const ExplanationPanel = ({ explanations }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!explanations || explanations.length === 0) return null;

  return (
    <div className="explanation-panel">
      <button 
        className="explanation-toggle" 
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span className="explanation-toggle-text">Reasoning</span>
        <span className="explanation-toggle-icon">{isOpen ? "▲" : "▼"}</span>
      </button>
      
      <div className={`explanation-content ${isOpen ? 'is-open' : ''}`}>
        <div className="explanation-content-inner">
           <ExplanationList explanations={explanations} />
        </div>
      </div>
    </div>
  );
};

export default ExplanationPanel;
