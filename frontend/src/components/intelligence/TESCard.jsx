import React from "react";
import RiskBadge from "./RiskBadge";
import RiskMeter from "./RiskMeter";

const TESCard = ({ tes, riskLevel, riskScore }) => {
  return (
    <div className="tes-card">
      <div className="tes-card__header">
        <div className="tes-card__title">
          <span className="tes-card__label">Threat Escalation Score</span>
          <span className="tes-card__value">{tes.toFixed(4)}</span>
        </div>
        <RiskBadge level={riskLevel} />
      </div>
      
      <div className="tes-card__meter-section">
        <div className="tes-card__meter-labels">
          <span className="tes-card__meter-label">Risk Score</span>
          <span className="tes-card__meter-value">{riskScore.toFixed(2)}</span>
        </div>
        <RiskMeter score={riskScore} level={riskLevel} />
      </div>
    </div>
  );
};

export default TESCard;
