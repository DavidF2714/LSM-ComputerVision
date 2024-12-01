from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import nbimporter
import os
import cv2
import mediapipe as mp
import numpy as np
from io import BytesIO
from PIL import Image
import sys
import base64
import torch
import joblib
from torchvision.models import EfficientNet_B4_Weights

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Miscellaneous import cropped_images
from Utils.LSM_Model import LSMCnnModel
import model as m

weights = EfficientNet_B4_Weights.IMAGENET1K_V1
preprocess_transform = weights.transforms()

mp_hands = mp.solutions.hands

# Load the trained model
model = joblib.load('model/lsm_cnn_model.pkl')

app = Flask(__name__)

CORS(app, resources = {r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def home():
    return "Welcome to the Flask Server for image predictions!"

@app.route("/api/predict/sign", methods=["POST"])
def crop():
    # Check if a file is included
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Load the image
    try:
        image = Image.open(file)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        return jsonify({"error": "Invalid image format"}), 400

    image_height, image_width, _ = image.shape

    cropped_image = None

    # Process with MediaPipe
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_hand_landmarks:
            return jsonify({"error": "No hands detected in the image"}), 400

        # Get bounding box for the first detected hand
        hand_landmarks = results.multi_hand_landmarks[0]
        x_min, x_max, y_min, y_max = cropped_images.get_hand_bbox(hand_landmarks, image_width, image_height)

        # Crop the image
        cropped_image = image[y_min:y_max, x_min:x_max]
    
    ### START 
    # img = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)).convert("RGB")

    # Preprocesa la imagen de prueba para el modelo
    preprocessed_image = preprocess_transform(cropped_pil_image).unsqueeze(0)

    # Cambia el modelo a modo de evaluación
    model.eval()

    # Predice la clase de la imagen
    with torch.no_grad():
        prediction = model(preprocessed_image)

    # Obtén la clase predicha
    predicted_class = torch.argmax(prediction).item()

     # Convert cropped PIL image to Base64
    buffered = BytesIO()
    cropped_pil_image.save(buffered, format="JPEG")
    cropped_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return the prediction and the cropped image as a JSON response
    return jsonify({
        'prediction': predicted_class,
        'cropped_image': f"data:image/jpeg;base64,{cropped_image_base64}"
    })


if __name__ == '__main__':
    app.run(debug=True, host="10.49.12.59", port = 1337)
