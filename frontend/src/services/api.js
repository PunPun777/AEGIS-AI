import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const analyseText = async (text) => {
  const response = await apiClient.post("/predict", { text });
  return response.data;
};
