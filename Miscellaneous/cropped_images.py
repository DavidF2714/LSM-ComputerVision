import os
import cv2
import mediapipe as mp
import numpy as np
import csv

# Inicialización de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Directorios de entrada y salida
IMAGE_FOLDER = 'LSM.v1i.yolov11/images_sorted'
OUTPUT_FOLDER = 'LSM_Hand_Crops/imagev2'

# Asegurarse de que el directorio de salida exista
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Archivo CSV para guardar información
CSV_FILE = 'hand_crop_info.csv'

# Crear el archivo CSV con los encabezados
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image_name', 'hands_found', 'left_hand_landmarks', 'cropped_hand'])

# Función para obtener el bounding box
# Función para obtener el bounding box con márgenes adicionales
def get_hand_bbox(landmarks, image_width, image_height, margin=20):
    x_coords = [lm.x for lm in landmarks.landmark]
    y_coords = [lm.y for lm in landmarks.landmark]
    
    # Calcular los límites iniciales del bounding box
    x_min = int(min(x_coords) * image_width)
    x_max = int(max(x_coords) * image_width)
    y_min = int(min(y_coords) * image_height)
    y_max = int(max(y_coords) * image_height)
    
    # Agregar márgenes
    x_min = max(x_min - margin, 0)
    x_max = min(x_max + margin, image_width)
    y_min = max(y_min - margin, 0)
    y_max = min(y_max + margin, image_height)
    
    # Ajustar el bounding box para hacerlo cuadrado
    bbox_width = x_max - x_min
    bbox_height = y_max - y_min
    bbox_size = max(bbox_width, bbox_height)
    
    # Centrar el cuadrado alrededor del bounding box inicial
    x_center = (x_min + x_max) // 2
    y_center = (y_min + y_max) // 2
    x_min = max(x_center - bbox_size // 2, 0)
    x_max = min(x_center + bbox_size // 2, image_width)
    y_min = max(y_center - bbox_size // 2, 0)
    y_max = min(y_center + bbox_size // 2, image_height)
    
    return x_min, x_max, y_min, y_max

# Procesar imágenes
with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
    for root, dirs, files in os.walk(IMAGE_FOLDER):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):
                # Leer imagen
                image_path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(image_path))  # Extraer etiqueta del subdirectorio
                image = cv2.imread(image_path)
                image_height, image_width, _ = image.shape
                
                # Procesar la imagen con MediaPipe
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                hands_found = 0
                cropped_hand = None
                left_landmarks = None
                
                if results.multi_hand_landmarks:
                    hands_found = len(results.multi_hand_landmarks)
                    
                    for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        # Determinar si la mano es izquierda
                        handedness = results.multi_handedness[hand_idx].classification[0].label
                        if handedness == 'Left':
                            left_landmarks = hand_landmarks.landmark
                            
                            # Obtener bounding box y recortar
                            x_min, x_max, y_min, y_max = get_hand_bbox(hand_landmarks, image_width, image_height)
                            cropped_image = image[y_min:y_max, x_min:x_max]
                            
                            # Guardar imagen recortada en la carpeta correspondiente
                            output_label_folder = os.path.join(OUTPUT_FOLDER, label)
                            os.makedirs(output_label_folder, exist_ok=True)
                            
                            output_image_path = os.path.join(output_label_folder, f'{file[:-4]}_Left.jpg')
                            cv2.imwrite(output_image_path, cropped_image)
                            
                            cropped_hand = 'Left'
                            break  # Procesar solo la primera mano izquierda encontrada
                
                # Guardar información en el CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([file, hands_found, left_landmarks, cropped_hand])
