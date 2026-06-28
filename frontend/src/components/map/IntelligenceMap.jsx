import React, { useState } from "react";
import { MapContainer, TileLayer, Circle, ZoomControl } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import RegionPopup from "./RegionPopup";
import RiskLegend from "./RiskLegend";
import MapControls from "./MapControls";

const REGION_COORDS = {
  "Middle East": [29.2985, 42.5510],
  "South Asia": [20.5937, 78.9629],
  "Europe": [54.5260, 15.2551],
  "USA": [37.0902, -95.7129],
  "Other": [0, 0],
};

const RISK_COLORS = {
  LOW: "#22c55e",
  MODERATE: "#eab308",
  HIGH: "#f97316",
  CRITICAL: "#ef4444",
};

const IntelligenceMap = ({ mapData }) => {
  const [isFullscreen, setIsFullscreen] = useState(false);

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  return (
    <div className={`map-wrapper ${isFullscreen ? "fullscreen" : ""}`}>
      <MapContainer
        center={[30, 0]}
        zoom={2.5}
        zoomControl={false}
        className="intelligence-map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          className="map-tiles"
        />
        <ZoomControl position="bottomright" />

        {mapData &&
          mapData.map((region) => {
            const coords = REGION_COORDS[region.region] || [0, 0];
            const color = RISK_COLORS[region.risk_level] || RISK_COLORS["LOW"];
            
            // Skip rendering "Other" region on the map if coordinates are [0,0]
            // just to avoid placing a random circle in the ocean, unless it's intended.
            // But we'll render it at [0,0] for now if it exists.

            return (
              <Circle
                key={region.region}
                center={coords}
                radius={1200000}
                pathOptions={{
                  color: color,
                  fillColor: color,
                  fillOpacity: 0.35,
                  weight: 2,
                }}
              >
                <RegionPopup data={region} />
              </Circle>
            );
          })}
      </MapContainer>
      <RiskLegend />
      <MapControls
        onToggleFullscreen={toggleFullscreen}
        isFullscreen={isFullscreen}
      />
    </div>
  );
};

export default IntelligenceMap;
