import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Punto di mount dell'app React
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);