import { useState } from "react";
import InputBox from "./InputBox";
import ResultCard from "./ResultCard";
import { fetchNewsAnalysis, predictText } from "../services/api";

const MainInterface = () => {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [newsResults, setNewsResults] = useState({});
  const [loadingNews, setLoadingNews] = useState(false);

  const handleFetchNews = async () => {
    try {
      setLoadingNews(true);
      const response = await fetchNewsAnalysis();
      setNewsResults(response.data);
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
    setPrediction(null);
    setLoading(true);

    try {
      const response = await predictText(text.trim());
      setPrediction(response.data.prediction);
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
        {prediction && (
          <section className="interface-section" aria-label="Analysis result">
            <ResultCard prediction={prediction} />
          </section>
        )}
      </div>

      {/* Right Column / Live News Section */}
      <div className="layout-column">
        <section className="card interface-section news-section" aria-label="Live News Analysis">
          <div className="news-header">
          <h2>Live News</h2>
          <button 
            className="analyse-btn" 
            onClick={handleFetchNews} 
            disabled={loadingNews}
          >
            {loadingNews ? <span className="spinner"></span> : "Analyze Live News"}
          </button>
        </div>

        {loadingNews ? (
          <div className="news-loading">Loading...</div>
        ) : (
          Object.keys(newsResults).length > 0 && (
            <div className="regions-container">
              {/* Region Group */}
              {Object.entries(newsResults).map(([region, data]) => {
                const tesScore = data.TES;
                let tesColorClass = "tes--green";
                if (tesScore > 0.7) tesColorClass = "tes--red";
                else if (tesScore >= 0.4) tesColorClass = "tes--orange";

                return (
                  /* Region Card */
                  <div key={region} className="region-card">
                    {/* TES Section */}
                    <div className="region-header-row">
                      <h3 className="region-title">{region}</h3>
                      <div className={`tes-badge ${tesColorClass}`}>
                        <span className="tes-label">TES</span>
                        <span className="tes-value">{tesScore.toFixed(2)}</span>
                      </div>
                    </div>
                    
                    {/* Event List */}
                    <div className="news-results">
                      {data.events.map((news, index) => (
                        <div key={index} className={`news-card news-card--${news.prediction.toLowerCase()}`}>
                          <h4>{news.title}</h4>
                          <span className="news-card__badge">{news.prediction}</span>
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
  );
};

export default MainInterface;
