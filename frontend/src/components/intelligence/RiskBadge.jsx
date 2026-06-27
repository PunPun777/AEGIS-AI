import React from "react";

const RiskBadge = ({ level }) => {
  const colorClass = `risk--${level.toLowerCase()}`;
  
  return (
    <span className={`risk-badge ${colorClass}`}>
      {level} RISK
    </span>
  );
};

export default RiskBadge;
