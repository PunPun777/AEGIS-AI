import React from "react";

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

const ResultCard = ({ prediction }) => {
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
        <span className="result-card__severity">{meta.severity}</span>
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

      {/* Confidence bar (decorative UX element) */}
      <div className="result-card__bar-wrap" aria-hidden="true">
        <div className="result-card__bar" />
      </div>
    </div>
  );
};

export default ResultCard;
