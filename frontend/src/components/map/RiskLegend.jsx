import React from "react";

const RiskLegend = () => {
  const legendItems = [
    { label: "Low", color: "#22c55e" },
    { label: "Moderate", color: "#eab308" },
    { label: "High", color: "#f97316" },
    { label: "Critical", color: "#ef4444" },
  ];

  return (
    <div className="risk-legend">
      <h4 className="risk-legend-title">Risk Level</h4>
      <div className="risk-legend-items">
        {legendItems.map((item) => (
          <div key={item.label} className="legend-item">
            <span
              className="color-box"
              style={{ backgroundColor: item.color }}
            ></span>
            <span className="legend-label">{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RiskLegend;
