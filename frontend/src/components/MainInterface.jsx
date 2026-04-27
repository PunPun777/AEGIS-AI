import React, { useState } from "react";
import InputBox from "./InputBox";
import ResultCard from "./ResultCard";
import { analyseText } from "../services/api";

const MainInterface = () => {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyse = async () => {
    // --- Validation ---
    if (!text.trim()) {
      setError("Please enter some text before analysing.");
      return;
    }

    setError("");
    setPrediction(null);
    setLoading(true);

    try {
      const data = await analyseText(text.trim());
      setPrediction(data.prediction);
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
  );
};

export default MainInterface;
