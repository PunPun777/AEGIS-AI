import React from "react";

const TESBadge = ({ tesScore }) => {
  let riskCategory = "Low";
  let colorClass = "tes--low";

  if (tesScore >= 1.0) {
    riskCategory = "Critical";
    colorClass = "tes--critical";
  } else if (tesScore >= 0.7) {
    riskCategory = "High";
    colorClass = "tes--high";
  } else if (tesScore >= 0.4) {
    riskCategory = "Moderate";
    colorClass = "tes--moderate";
  }

  return (
    <div className={`tes-indicator ${colorClass}`}>
      <div className="tes-badge">
        <span className="tes-label">TES</span>
        <span className="tes-value">{tesScore.toFixed(2)}</span>
      </div>
      <div className="tes-category">{riskCategory} Risk</div>
    </div>
  );
};

export default TESBadge;
