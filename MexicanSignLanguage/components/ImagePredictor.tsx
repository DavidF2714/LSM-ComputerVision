"use client"
import { useState, useRef, useEffect } from "react";
import Webcam from "react-webcam";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  LinearProgress,
  Alert
} from "@mui/material";


export default function TryItOut() {
  const [isRecording, setIsRecording] = useState(false);
  const [countdown, setCountdown] = useState(5);
  const [progress, setProgress] = useState(0);
  const [currentSign, setCurrentSign] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [notification, setNotification] = useState("");
  const [openDialog, setOpenDialog] = useState(false);
  const [webcamActive, setWebcamActive] = useState(false);
  const [cameraError, setCameraError] = useState(""); // To display camera error messages
  const webcamRef = useRef(null);

  const handleOpenDialog = async () => {
    // Check for camera permissions
    try {
      await navigator.mediaDevices.getUserMedia({ video: true });
      setOpenDialog(true); // Open the dialog if permission is granted
      setCameraError("");
    } catch (error) {
      setCameraError(
        "Camera permission is required to use this feature. Please enable it in your browser settings."
      );
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setWebcamActive(true); // Activate webcam
    setIsRecording(true);
    setCountdown(5);
    setNotification(
      "The webcam will start recording. When the countdown is 0, raise your hand and show the sign!"
    );
  };

  // Capture image and send it to the server
  const captureAndPredict = async () => {
    if (!webcamRef.current) return;

    const image = webcamRef.current.getScreenshot();
    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image }),
      });

      const data = await response.json();
      if (response.ok) {
        setPredictions((prev) => [...prev, data.prediction]);
      } else {
        console.error("Prediction failed:", data.message);
      }
    } catch (error) {
      console.error("Error sending image to server:", error);
    }
  };

  // Countdown and progress bar logic
  useEffect(() => {
    let interval;

    if (isRecording) {
      if (countdown > 0) {
        setNotification(`Countdown: ${countdown}`);
        interval = setTimeout(() => setCountdown(countdown - 1), 1000);
      } else {
        setNotification("Webcam recording started!");
        setProgress(0);

        // Start progress-based logic
        const progressInterval = setInterval(() => {
          setProgress((prev) => {
            const nextProgress = prev + 20;

            // Every 5 seconds, notify user and capture image
            if (nextProgress === 80) {
              setNotification("Hold the sign steady...");
            }
            if (nextProgress === 100) {
              captureAndPredict();
              setNotification("Change the sign!");
            }

            if (nextProgress >= 100) return 0; // Reset progress bar
            return nextProgress;
          });
        }, 1000);

        // Stop recording after 30 seconds
        setTimeout(() => {
          clearInterval(progressInterval);
          setIsRecording(false);
          setNotification("Recording stopped.");
        }, 30000);
      }
    }

    return () => clearInterval(interval);
  }, [isRecording, countdown]);

  return (
    // <div
    //   style={{
    //     textAlign: "center",
    //     padding: "20px",
    //     minHeight: "100vh",
    //   }}
    // >
    <section id="predictionTool" style={{textAlign:"center"}}>
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
      <div className="py-12 md:py-20 border-t border-gray-800">
      <div className="max-w-3xl mx-auto text-center pb-12 md:pb-20">
            <h2 className="h2 mb-4">Prueba la Herramienta</h2>
            <p className="text-xl text-gray-400">Explora nuestra herramienta de Prueba. ¡Muestra las señas que corresponden al alfabeto de LSM y obtén la predicción!</p>
      </div>
      {notification && <Typography variant="h6">{notification}</Typography>}
      <div style={{ marginBottom: "20px" }}>
        {webcamActive ? (
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            style={{
              width: "400px",
              height: "400px",
              borderRadius: "10px",
              boxShadow: "0 4px 10px rgba(0, 0, 0, 0.3)",
              display: "block", // Centers webcam
              margin: "0 auto",
            }}
          />
        ) : (
          <img
            src="https://lloydsofindiana.com/image/cache/placeholder-638x638.png"// Use imported placeholder image
            alt="Webcam Placeholder"
            style={{
              width: "400px",
              height: "400px",
              borderRadius: "10px",
              boxShadow: "0 4px 10px rgba(0, 0, 0, 0.3)",
              display: "block",
              margin: "0 auto",
            }}
          />
        )}
        {isRecording && (
          <div style={{ width: "400px", margin: "10px auto" }}>
            <LinearProgress variant="determinate" value={progress} />
          </div>
        )}
      </div>
      <div>
        {!isRecording && (
          <Button
            variant="contained"
            color="primary"
            onClick={handleOpenDialog}
            style={{
              padding: "10px 20px",
              fontSize: "1rem",
              borderRadius: "5px",
              backgroundColor: "#007bff",
            }}
          >
            Try It Out
          </Button>
        )}
      </div>
      {cameraError && (
        <Alert severity="error" style={{ marginTop: "20px" }}>
          {cameraError}
        </Alert>
      )}
      <div style={{ marginTop: "20px" }}>
        <h3>Predictions:</h3>
        {predictions.length > 0 ? (
          predictions.map((prediction, index) => (
            <Typography key={index}>
              Sign {index + 1}: {prediction}
            </Typography>
          ))
        ) : (
          <Typography>No predictions yet</Typography>
        )}
      </div>

      {/* MUI Dialog for Instructions */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Get Ready!</DialogTitle>
        <DialogContent>
          <Typography>
            The webcam will start recording. When the countdown is 0, raise your
            hand and show the sign you want predicted!
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={handleCloseDialog}
            variant="contained"
            color="primary"
          >
            Start
          </Button>
        </DialogActions>
       </Dialog>
       </div>
       </div>
      </section>
  );
}