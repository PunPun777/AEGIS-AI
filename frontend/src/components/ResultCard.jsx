import React from "react";
import ConfidenceIndicator from "./ConfidenceIndicator";
import SeverityBadge from "./SeverityBadge";
import ExplanationPanel from "./intelligence/ExplanationPanel";

/** Maps prediction labels to display metadata */
const PREDICTION_META = {
  conflict: {
    label: "CONFLICT",
    icon: "🔴",
    description:
      "High-risk geopolitical conflict activity detected. Immediate threat assessment recommended.",
    severity: "CRITICAL",
  },
  protest: {
    label: "PROTEST",
    icon: "🟠",
    description:
      "Civil unrest or protest activity identified. Monitor for escalation patterns.",
    severity: "MODERATE",
  },
  normal: {
    label: "NORMAL",
    icon: "🟢",
    description:
      "No significant threat indicators detected. Situation appears stable.",
    severity: "STABLE",
  },
};

const ResultCard = ({ prediction, confidence, severity, explanation }) => {
  const meta = PREDICTION_META[prediction] ?? {
    label: prediction?.toUpperCase() ?? "UNKNOWN",
    icon: "⚪",
    description: "Unrecognised prediction class returned by the model.",
    severity: "UNKNOWN",
  };

  return (
    <div className={`result-card result-card--${prediction}`} role="status">
      {/* Header */}
      <div className="result-card__header">
        <span className="result-card__badge">ANALYSIS COMPLETE</span>
      </div>

      {/* Icon + Label */}
      <div className="result-card__main">
        <span className="result-card__icon" aria-hidden="true">
          {meta.icon}
        </span>
        <h2 className="result-card__label">{meta.label}</h2>
      </div>

      {/* Description */}
      <p className="result-card__description">{meta.description}</p>

      {/* Meta Indicators */}
      <div className="result-card__meta-wrapper">
        <SeverityBadge severity={severity || meta.severity} />
        {confidence !== undefined && <ConfidenceIndicator confidence={confidence} />}
      </div>
      
      <ExplanationPanel explanations={explanation} />
    </div>
  );
};

export default ResultCard;
