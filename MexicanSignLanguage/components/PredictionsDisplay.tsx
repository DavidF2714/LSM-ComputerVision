import React from "react";
import Image from "next/image";
import { Typography, Box, Card, CardContent } from "@mui/material";
import {signs } from '../Utils/signs'

const PredictionsDisplay = ({ predictions }) => {
  return (
    <Box sx={{ width: "100%", padding: 2 }}>
      {predictions.length > 0 ? (
        predictions.map((p, index) => {
          // Find the corresponding sign
          const matchingSign = signs.find((sign) => sign.id === p.prediction);

          return (
            <Box
              key={index}
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                border: "1px solid #ccc",
                borderRadius: "8px",
                marginBottom: 3,
                padding: 2,
              }}
            >
              {/* Left Section: Cropped Image with Title */}
              <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Typography variant="subtitle1" sx={{ fontWeight: "bold", marginBottom: 1 }}>
                Seña a Predecir
                </Typography>
                <img
                  src={p.croppedImage}
                  alt={`Seña a Predecir ${index}`}
                  style={{ width: "100px", height: "100px", objectFit: "cover", borderRadius: "8px" }}
                />
                <Typography variant="body1" sx={{ marginTop: 1 }}>
                  Class: {p.prediction}
                </Typography>
              </Box>

              {/* Middle Section: Predicted Letter with Title */}
              <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Typography variant="subtitle1" sx={{ fontWeight: "bold", marginBottom: 1 }}>
                  Letra Predicha
                </Typography>
                <Card sx={{ minWidth: 100, padding: 1, textAlign: "center", boxShadow: 3 }}>
                  <CardContent>
                    <Typography variant="h4" color="primary">
                      {matchingSign?.letter || "?"}
                    </Typography>
                  </CardContent>
                </Card>
              </Box>

              {/* Right Section: Predicted Sign Image with Title */}
              <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Typography variant="subtitle1" sx={{ fontWeight: "bold", marginBottom: 1 }}>
                  Seña Predicha
                </Typography>
                {matchingSign && (
                  <Image
                    src={matchingSign.image}
                    alt={`Sign ${matchingSign.letter}`}
                    width={100}
                    height={100}
                    style={{ borderRadius: "8px" }}
                  />
                )}
              </Box>
            </Box>
          );
        })
      ) : (
        <Typography>Sin Predicciones</Typography>
      )}
    </Box>
  );
};

export default PredictionsDisplay;
