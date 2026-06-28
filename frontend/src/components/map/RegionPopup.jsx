import React from "react";
import { Popup } from "react-leaflet";

const RegionPopup = ({ data }) => {
  return (
    <Popup className="region-popup">
      <div className="region-popup-content">
        <h3>{data.region}</h3>
        <div className="popup-stat">
          <span className="stat-label">TES:</span>
          <span className="stat-value tes-value">{data.tes.toFixed(2)}</span>
        </div>
        <div className="popup-stat">
          <span className="stat-label">Risk Level:</span>
          <span className={`stat-value risk-${data.risk_level.toLowerCase()}`}>
            {data.risk_level}
          </span>
        </div>
        <div className="popup-stat">
          <span className="stat-label">Trend:</span>
          <span className={`stat-value trend-${data.trend}`}>
            {data.trend === "increasing" ? "↑" : data.trend === "decreasing" ? "↓" : "→"} {data.trend}
          </span>
        </div>
        <div className="popup-stat">
          <span className="stat-label">Events:</span>
          <span className="stat-value">{data.event_count}</span>
        </div>
        <div className="popup-stat">
          <span className="stat-label">Avg Confidence:</span>
          <span className="stat-value">{(data.confidence_average * 100).toFixed(1)}%</span>
        </div>
        
        <div className="popup-severity">
          <h4>Severity Distribution</h4>
          <ul>
            <li><span className="sev-dot sev-critical"></span>Critical: {data.severity_distribution.CRITICAL}</li>
            <li><span className="sev-dot sev-high"></span>High: {data.severity_distribution.HIGH}</li>
            <li><span className="sev-dot sev-medium"></span>Medium: {data.severity_distribution.MEDIUM}</li>
            <li><span className="sev-dot sev-low"></span>Low: {data.severity_distribution.LOW}</li>
          </ul>
        </div>
      </div>
    </Popup>
  );
};

export default RegionPopup;
