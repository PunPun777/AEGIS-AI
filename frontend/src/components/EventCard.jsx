import React from "react";
import ConfidenceIndicator from "./ConfidenceIndicator";
import SeverityBadge from "./SeverityBadge";
import ExplanationPanel from "./intelligence/ExplanationPanel";
import HybridDecisionPanel from "./intelligence/HybridDecisionPanel";
import DiagnosticsPanel from "./intelligence/DiagnosticsPanel";

const EventCard = ({ news }) => {
  return (
    <div className={`news-card news-card--${news.prediction?.toLowerCase()}`}>
      <div className="news-card__header">
        <span className="news-card__badge">{news.prediction}</span>
        {news.overridden && (
          <span className="news-card__hybrid-badge">HYBRID OVERRIDE</span>
        )}
      </div>
      <h4 className="news-card__title">{news.title}</h4>
      <div className="news-card__meta-wrapper">
        <SeverityBadge severity={news.severity} />
        <ConfidenceIndicator confidence={news.confidence} />
      </div>
      <ExplanationPanel explanations={news.explanation} />
      <HybridDecisionPanel 
        overridden={news.overridden}
        originalPrediction={news.original_prediction}
        reason={news.override_reason}
        categories={news.matched_categories}
        keywords={news.matched_keywords}
      />
      <DiagnosticsPanel diagnostics={news._diagnostics} />
    </div>
  );
};

export default EventCard;
