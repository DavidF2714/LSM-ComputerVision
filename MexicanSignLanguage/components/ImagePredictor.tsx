"use client";
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
  Alert,
} from "@mui/material";
import { GetPrediction } from "../Service/predictService";
import { base64ToFile } from "../Utils/helper";
import Image from "next/image";
import PredictionsDisplay from "./PredictionsDisplay";

export default function TryItOut() {
  const [isRecording, setIsRecording] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentSign, setCurrentSign] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [notification, setNotification] = useState("");
  const [openDialog, setOpenDialog] = useState(false);
  const [webcamActive, setWebcamActive] = useState(false);
  const [cameraError, setCameraError] = useState(""); // To display camera error messages
  const webcamRef = useRef(null);
  const [isPredicting, setIsPredicting] = useState(false);

  const handleOpenDialog = async () => {
    // Check for camera permissions
    try {
      await navigator.mediaDevices.getUserMedia({ video: true });
      setOpenDialog(true); // Open the dialog if permission is granted
      setCameraError("");
    } catch (error) {
      setCameraError(
        "Se requiere permiso de la cámara para usar esta función. Por favor, actívalo en la configuración de tu navegador."
      );
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setWebcamActive(true); // Activate webcam
    setIsRecording(true);
    setNotification(
      "La cámara está activa. ¡Levanta tu mano y muestra la seña que quieres predecir!"
    );
  };

  const captureAndPredict = async () => {
    if (captureAndPredict.isRunning) return; // Prevent concurrent executions
    captureAndPredict.isRunning = true;

    try {
      if (!webcamRef.current) return;
      const image = webcamRef.current.getScreenshot();
      const imageFile = base64ToFile(image);

      const response = await GetPrediction(imageFile);
      const { cropped_image, prediction } = response;

      setPredictions((prev) => [
        { croppedImage: cropped_image, prediction },
        ...prev,
      ]);
    } catch (error) {
      console.error("Error during prediction:", error);
    } finally {
      captureAndPredict.isRunning = false; // Reset the flag
    }
  };
  captureAndPredict.isRunning = false;

  useEffect(() => {
    let interval;

    if (isRecording) {
      setNotification("La Cámara empezó a grabar!");

      // Start progress-based logic
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          const nextProgress = prev + 20;

          if (nextProgress === 80) {
            captureAndPredict();
            setNotification("Mantén la Seña!");
          }

          // Capture image at regular intervals
          if (nextProgress === 100) {
            setNotification("Cambia de Seña!");
          }

          if (nextProgress >= 100) return 0; // Reset progress bar
          return nextProgress;
        });
      }, 1000);

      // Save interval reference to clear later
      interval = progressInterval;
    }

    return () => clearInterval(interval);
  }, [isRecording]);

  const handleStopRecording = () => {
    setIsRecording(false);
    setNotification("Grabación detenida.");
  };

  return (
    <section id="predictionTool" style={{ textAlign: "center" }}>
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="py-12 md:py-20 border-t border-gray-800">
          <div className="max-w-3xl mx-auto text-center pb-12 md:pb-20">
            <h2 className="h2 mb-4">Prueba la Herramienta</h2>
            <p className="text-xl text-gray-400">
              Explora nuestra herramienta de Prueba. ¡Muestra las señas que
              corresponden al alfabeto de LSM y obtén la predicción!
            </p>
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
                src="https://lloydsofindiana.com/image/cache/placeholder-638x638.png" // Use imported placeholder image
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
            {!isRecording ? (
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
                Probar Herramienta
              </Button>
            ) : (
              <Button
                variant="contained"
                color="secondary"
                onClick={handleStopRecording}
                style={{
                  padding: "10px 20px",
                  fontSize: "1rem",
                  borderRadius: "5px",
                  backgroundColor: "#dc3545",
                }}
              >
                Detener
              </Button>
            )}
          </div>
          {cameraError && (
            <Alert severity="error" style={{ marginTop: "20px" }}>
              {cameraError}
            </Alert>
          )}
          <div style={{ marginTop: "20px" }}>
            <h3>Predicciones:</h3>
            <PredictionsDisplay predictions={predictions} />
          </div>
          <Dialog open={openDialog} onClose={handleCloseDialog}>
            <DialogTitle>¡Prepárate!</DialogTitle>
            <DialogContent>
              <Typography>
                La cámara comenzará a grabar. Muestra la seña que quieres
                predecir.
              </Typography>
            </DialogContent>
            <DialogActions>
              <Button
                onClick={handleCloseDialog}
                variant="contained"
                color="primary"
              >
                Comenzar
              </Button>
            </DialogActions>
          </Dialog>
        </div>
      </div>
    </section>
  );
}
