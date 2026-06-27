import React from "react";
import ExplanationItem from "./ExplanationItem";

const ExplanationList = ({ explanations }) => {
  if (!explanations || explanations.length === 0) return null;

  return (
    <ul className="explanation-list">
      {explanations.map((text, idx) => (
        <ExplanationItem key={idx} text={text} />
      ))}
    </ul>
  );
};

export default ExplanationList;
