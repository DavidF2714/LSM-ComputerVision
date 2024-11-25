"use client"
import { useState, useRef } from "react";
import Webcam from "react-webcam";
import styles from "../app/css/additional-styles/TryItOut.module.css"; // Create a CSS module for styling

export default function TryItOut() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const webcamRef = useRef(null);

  const captureImage = () => {
    if (webcamRef.current) {
      const screenshot = webcamRef.current.getScreenshot();
      setImage(screenshot);
      setPrediction(null); // Reset prediction if a new image is captured
    }
  };

  const handlePrediction = async () => {
    if (!image) return alert("Please capture an image first!");

    setLoading(true);
    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image }),
      });

      const data = await response.json();
      if (response.ok) {
        setPrediction(data.prediction);
      } else {
        alert("Prediction failed: " + data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while predicting.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Try It Out</h1>
      <div className={styles.webcamContainer}>
        <Webcam
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className={styles.webcam}
        />
        <button className={styles.captureButton} onClick={captureImage}>
          Capture Image
        </button>
      </div>
      {image && (
        <div className={styles.imagePreview}>
          <h3 className={styles.subtitle}>Captured Image:</h3>
          <img src={image} alt="Captured" className={styles.previewImage} />
        </div>
      )}
      <div>
        <button
          className={`${styles.predictButton} ${loading && styles.disabled}`}
          onClick={handlePrediction}
          disabled={loading}
        >
          {loading ? "Predicting..." : "Get Prediction"}
        </button>
      </div>
      {prediction && (
        <div className={styles.predictionResult}>
          <h3 className={styles.subtitle}>Prediction Result:</h3>
          <p className={styles.prediction}>{prediction}</p>
        </div>
      )}
    </div>
  );
}
