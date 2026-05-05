import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const predictText = (text) => API.post("/predict", { text });

export const fetchNewsAnalysis = () => API.get("/news-analysis");
