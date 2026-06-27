import React from "react";

const ExplanationItem = ({ text }) => {
  return (
    <li className="explanation-item">
      <span className="explanation-bullet">•</span>
      <span className="explanation-text">{text}</span>
    </li>
  );
};

export default ExplanationItem;
