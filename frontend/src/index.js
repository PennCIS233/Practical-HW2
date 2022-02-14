import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import ConnectPage from "./pages/ConnectPage";
import ElectionPage from "./pages/ElectionPage";

ReactDOM.render(
  <div>
    <Router>
      <Routes>
        <Route path="/" element={<ConnectPage />} />
        <Route path="/election" element={<ElectionPage />} />
      </Routes>
    </Router>
  </div>,
  document.getElementById("root")
);
