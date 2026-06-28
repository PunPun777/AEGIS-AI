import { useState } from "react";
import InputBox from "./InputBox";
import ResultCard from "./ResultCard";
import ConfidenceIndicator from "./ConfidenceIndicator";
import SeverityBadge from "./SeverityBadge";
import TESCard from "./intelligence/TESCard";
import ExplanationPanel from "./intelligence/ExplanationPanel";
import { fetchNewsAnalysis, predictText, fetchIntelligenceMap } from "../services/api";
import IntelligenceMap from "./map/IntelligenceMap";

const MainInterface = () => {
  const [text, setText] = useState("");
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [newsResults, setNewsResults] = useState({});
  const [loadingNews, setLoadingNews] = useState(false);
  const [mapData, setMapData] = useState(null);

  const handleFetchDashboard = async () => {
    try {
      setLoadingNews(true);
      const [newsRes, mapRes] = await Promise.all([
        fetchNewsAnalysis(),
        fetchIntelligenceMap()
      ]);
      setNewsResults(newsRes.data);
      setMapData(mapRes.data.regions);
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingNews(false);
    }
  };

  const handleAnalyse = async () => {
    if (!text.trim()) {
      setError("Please enter some text before analysing.");
      return;
    }

    setError("");
    setPredictionResult(null);
    setLoading(true);

    try {
      const response = await predictText(text.trim());
      setPredictionResult(response.data);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Unable to reach the AEGIS-AI backend. Ensure the server is running on port 8000.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      {/* Top Map Section */}
      <section className="dashboard-map-section">
        <div className="map-header">
          <h2>Global Intelligence Map</h2>
          <button 
            className="analyse-btn" 
            onClick={handleFetchDashboard} 
            disabled={loadingNews}
          >
            {loadingNews ? <span className="spinner"></span> : "Refresh Dashboard"}
          </button>
        </div>
        <div className="map-container-wrapper card">
          {loadingNews ? (
             <div className="map-loading">Loading Map Data...</div>
          ) : mapData ? (
             <IntelligenceMap mapData={mapData} />
          ) : (
             <div className="map-placeholder">Click 'Refresh Dashboard' to load intelligence map.</div>
          )}
        </div>
      </section>

      {/* Bottom Sections */}
      <div className="interface-layout">
        {/* Left Column */}
        <div className="layout-column">
          {/* Input Section */}
          <section className="card interface-section" aria-label="Text input">
            <InputBox
              value={text}
              onChange={setText}
              onSubmit={handleAnalyse}
              loading={loading}
              error={error}
            />
          </section>

          {/* Result Section */}
          {predictionResult && (
            <section className="interface-section" aria-label="Analysis result">
              <ResultCard 
                prediction={predictionResult.prediction} 
                confidence={predictionResult.confidence} 
                severity={predictionResult.severity}
                explanation={predictionResult.explanation}
              />
            </section>
          )}
        </div>

        {/* Right Column / Live News Section */}
        <div className="layout-column">
          <section className="card interface-section news-section" aria-label="Live News Analysis">
            <div className="news-header">
              <h2>Live News Analysis</h2>
            </div>

            {loadingNews ? (
              <div className="news-loading">Loading...</div>
            ) : (
              Object.keys(newsResults).length > 0 && (
                <div className="regions-container">
                  {/* Region Group */}
                  {Object.entries(newsResults).map(([region, data]) => {
                    return (
                      /* Region Card */
                      <div key={region} className="region-card">
                        {/* Region Header Section */}
                        <div className="region-header-row">
                          <h3 className="region-title">{region}</h3>
                          <div className="region-indicators">
                            {/* Anomaly Section */}
                            {data.anomaly ? (
                              <div className="anomaly-badge anomaly-badge--true">
                                <span className="anomaly-label">Anomaly Detected</span>
                              </div>
                            ) : (
                              <div className="anomaly-badge anomaly-badge--false">
                                <span className="anomaly-label">Normal Activity</span>
                              </div>
                            )}
                            {/* TES Display */}
                            <TESCard 
                              tes={data.TES} 
                              riskLevel={data.risk_level} 
                              riskScore={data.risk_score} 
                            />
                            {/* Trend Section */}
                            <div className={`trend-badge trend-badge--${data.trend}`}>
                              <span className="trend-icon">
                                {data.trend === "increasing" ? "↑" : data.trend === "decreasing" ? "↓" : "→"}
                              </span>
                              <span className="trend-label">{data.trend}</span>
                            </div>
                          </div>
                        </div>
                        
                        {/* Event List */}
                        <div className="news-results">
                          {data.events.map((news, index) => (
                            <div key={index} className={`news-card news-card--${news.prediction.toLowerCase()}`}>
                              <div className="news-card__header">
                                <span className="news-card__badge">{news.prediction}</span>
                              </div>
                              <h4 className="news-card__title">{news.title}</h4>
                              <div className="news-card__meta-wrapper">
                                <SeverityBadge severity={news.severity} />
                                <ConfidenceIndicator confidence={news.confidence} />
                              </div>
                              <ExplanationPanel explanations={news.explanation} />
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default MainInterface;
