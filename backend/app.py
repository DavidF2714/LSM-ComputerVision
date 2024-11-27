from flask import Flask, request, jsonify, send_file
import nbimporter
import os
import cv2
import mediapipe as mp
import numpy as np
from io import BytesIO
from PIL import Image
import sys
import torch
from torchvision.datasets import ImageFolder
import joblib

print("asssssssssss: ", torch.cuda.is_available())

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Miscellaneous import cropped_images
from Utils.LSM_Model import LSMCnnModel
import model as m

mp_hands = mp.solutions.hands

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model
# model = joblib.load('model/lsm_cnn_model.pkl')
model = torch.load('model/lsm_cnn_model.pkl', map_location=torch.device('cpu'))

# device = torch.device("cpu")
# model = model.to(device)
# model.eval()

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Server for image predictions!"

@app.route("/crop/test", methods=["POST"])
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
    img = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
   
    # Preprocesa la imagen de prueba para el modelo
    preprocessed_image = m.preprocess_transform(img).unsqueeze(0)

    # Cambia el modelo a modo de evaluación
    model.eval()

    # Predice la clase de la imagen
    with torch.no_grad():
        prediction = model(preprocessed_image)

    # Obtén la clase predicha
    predicted_class = torch.argmax(prediction).item()

      # Return the prediction as a JSON response
    return jsonify({'prediction class': predicted_class})
        
        # # Convert cropped image to bytes for response
        # _, buffer = cv2.imencode('.jpg', cropped_image)
        # cropped_image_bytes = BytesIO(buffer)

        # return send_file(cropped_image_bytes, mimetype='image/jpeg', as_attachment=False)



if __name__ == '__main__':
    app.run(debug=True, port = 3000)
