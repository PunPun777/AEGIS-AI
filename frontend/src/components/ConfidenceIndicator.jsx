import React from "react";

const ConfidenceIndicator = ({ confidence }) => {
  const percentage = (confidence * 100).toFixed(2);
  let colorClass = "confidence--red";
  if (confidence >= 0.9) colorClass = "confidence--green";
  else if (confidence >= 0.7) colorClass = "confidence--yellow";

  return (
    <div className={`confidence-indicator ${colorClass}`}>
      <div className="confidence-indicator__header">
        <span className="confidence-indicator__label">Confidence</span>
        <span className="confidence-indicator__value">{percentage}%</span>
      </div>
      <div className="confidence-indicator__bar-bg">
        <div 
          className="confidence-indicator__bar-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ConfidenceIndicator;
