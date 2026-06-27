import React from "react";

const RiskMeter = ({ score, level }) => {
  // Max TES is 1.5, calculate percentage for the meter fill
  const percentage = Math.min((score / 1.5) * 100, 100);
  const colorClass = `risk-meter--${level.toLowerCase()}`;
  
  return (
    <div className={`risk-meter ${colorClass}`}>
      <div className="risk-meter__track">
        <div 
          className="risk-meter__fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default RiskMeter;
