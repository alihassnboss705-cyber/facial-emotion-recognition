
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("Checking...");

  // Check backend health
  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => {
        if (!res.ok) throw new Error("API unavailable");
        return res.json();
      })
      .then(() => setApiStatus("Connected"))
      .catch(() => setApiStatus("Offline"));
  }, []);

  // Handle image selection
  function handleFile(e) {
    const selected = e.target.files[0];

    if (!selected) return;

    if (!selected.type.startsWith("image/")) {
      alert("Please select a valid image.");
      return;
    }

    if (selected.size > 5 * 1024 * 1024) {
      alert("Image must be smaller than 5 MB.");
      return;
    }

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  }

  // Send image to FastAPI
  async function detectEmotion() {
    if (!file) {
      alert("Please upload an image first.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed");
      }

      setResult(data);
    } catch (error) {
      setResult({
        detected: false,
        label: "ERROR",
        reason: error.message,
      });
    } finally {
      setLoading(false);
    }
  }

  function resetApp() {
    setFile(null);
    setPreview("");
    setResult(null);
  }

  return (
    <div className="app">

      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">AI</div>
          <span>Emotion<span className="accent">AI</span></span>
        </div>

        <div className="api-status">
          <span className={`status-dot ${apiStatus === "Connected" ? "online" : "offline"}`}></span>
          API {apiStatus}
        </div>
      </header>

      <main className="container">

        <section className="hero">
          <span className="eyebrow">ARTIFICIAL INTELLIGENCE</span>
          <h1>Facial Emotion <span>Recognition</span></h1>
          <p>
            Upload a facial image and let AI analyze the
            emotion using deep learning.
          </p>
        </section>

        <section className="workspace">

          <div className="panel upload-panel">
            <div className="panel-heading">
              <div>
                <h2>Upload Image</h2>
                <p>Select a clear facial photograph</p>
              </div>
              <span className="step-number">01</span>
            </div>

            <label className="upload-area">
              {preview ? (
                <img src={preview} alt="Uploaded face" className="preview-image" />
              ) : (
                <div className="upload-placeholder">
                  <div className="upload-icon">↑</div>
                  <h3>Drop your image here</h3>
                  <p>or click to browse files</p>
                  <span>JPG, PNG · Maximum 5 MB</span>
                </div>
              )}

              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleFile}
                hidden
              />
            </label>

            {file && (
              <div className="file-info">
                <span>📷 {file.name}</span>
                <button onClick={resetApp}>Remove</button>
              </div>
            )}

            <button
              className="detect-button"
              onClick={detectEmotion}
              disabled={!file || loading}
            >
              {loading ? "Analyzing..." : "✦  Detect Emotion"}
            </button>

            <p className="privacy-note">
              Your image is processed by your local AI backend.
            </p>
          </div>

          <div className="panel result-panel">
            <div className="panel-heading">
              <div>
                <h2>Analysis Result</h2>
                <p>AI prediction and confidence</p>
              </div>
              <span className="step-number">02</span>
            </div>

            {!result && (
              <div className="empty-result">
                <div className="result-icon">◉</div>
                <h3>Waiting for image</h3>
                <p>Your emotion analysis will appear here.</p>
              </div>
            )}

            {result && (
              <div className="result-content">
                <span className="result-label">DETECTED EMOTION</span>

                <h1 className={
                  result.detected && result.label !== "NO DETECTION"
                    ? "emotion-name"
                    : "error-name"
                }>
                  {result.label}
                </h1>

                {result.reason && (
                  <p className="reason">{result.reason}</p>
                )}

                {result.detected && result.label !== "NO DETECTION" && (
                  <>
                    <div className="confidence-box">
                      <div className="confidence-heading">
                        <span>Confidence Score</span>
                        <strong>
                          {(result.confidence * 100).toFixed(1)}%
                        </strong>
                      </div>

                      <div className="progress-track">
                        <div
                          className="progress-fill"
                          style={{
                            width: `${result.confidence * 100}%`,
                          }}
                        />
                      </div>
                    </div>

                    <div className="probabilities">
                      <h3>Emotion Probabilities</h3>

                      {Object.entries(result.probabilities || {}).map(
                        ([emotion, probability]) => (
                          <div className="probability-row" key={emotion}>
                            <span>{emotion}</span>

                            <div className="probability-track">
                              <div
                                className={`probability-fill ${
                                  emotion.toUpperCase() === result.label
                                    ? "highlight"
                                    : ""
                                }`}
                                style={{
                                  width: `${probability * 100}%`,
                                }}
                              />
                            </div>

                            <strong>
                              {(probability * 100).toFixed(1)}%
                            </strong>
                          </div>
                        )
                      )}
                    </div>
                  </>
                )}

                <button className="reset-button" onClick={resetApp}>
                  Analyze Another Image
                </button>
              </div>
            )}
          </div>

        </section>

        <footer>
          <p>EmotionAI · Powered by CNN & FastAPI</p>
          <span>AI Emotion Recognition System</span>
        </footer>

      </main>
    </div>
  );
}

export default App;
