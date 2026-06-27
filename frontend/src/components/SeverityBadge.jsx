import React from "react";

const SeverityBadge = ({ severity }) => {
  const normalized = severity?.toLowerCase() || "low";
  
  return (
    <div className={`severity-indicator severity--${normalized}`}>
      <div className="severity-indicator__header">
        <span className="severity-indicator__label">Severity</span>
        <span className="severity-indicator__value">{severity || "LOW"}</span>
      </div>
      <div className="severity-indicator__bar" />
    </div>
  );
};

export default SeverityBadge;
