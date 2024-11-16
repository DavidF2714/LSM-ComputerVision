import os
import cv2
import mediapipe as mp
import numpy as np
import csv

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Input and output directories
IMAGE_FOLDER = 'LSM.v1i.yolov11/images'
OUTPUT_FOLDER = 'LSM_Hand_Crops/Images'

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# CSV file for saving information
CSV_FILE = 'hand_crop_info.csv'

# Create the CSV file with headers
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image_name', 'hands_found', 'left_hand_landmarks', 'right_hand_landmarks', 'cropped_hand'])

# Function to get square bounding box
def get_square_bbox(x_min, x_max, y_min, y_max, image_width, image_height, margin=15):
    # Calculate width and height of the bounding box
    width = x_max - x_min
    height = y_max - y_min
    max_side = max(width, height)

    # Adjust the box to be square, keeping it centered
    center_x = (x_min + x_max) // 2
    center_y = (y_min + y_max) // 2

    # Calculate new square bounds
    square_x_min = max(center_x - max_side // 2 - margin, 0)
    square_x_max = min(center_x + max_side // 2 + margin, image_width)
    square_y_min = max(center_y - max_side // 2 - margin, 0)
    square_y_max = min(center_y + max_side // 2 + margin, image_height)

    return square_x_min, square_x_max, square_y_min, square_y_max

# Process images
with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
    for root, dirs, files in os.walk(IMAGE_FOLDER):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                # Read image
                image_path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(image_path))  # Extract label from the subdirectory
                image = cv2.imread(image_path)
                image_height, image_width, _ = image.shape

                # Process the image with MediaPipe
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                hands_found = 0
                cropped_hand = None
                left_landmarks, right_landmarks = None, None

                if results.multi_hand_landmarks:
                    hands_found = len(results.multi_hand_landmarks)

                    for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        # Determine if the hand is left or right
                        handedness = results.multi_handedness[hand_idx].classification[0].label
                        if handedness == 'Left':
                            left_landmarks = hand_landmarks.landmark
                        elif handedness == 'Right':
                            right_landmarks = hand_landmarks.landmark

                        # Get bounding box
                        x_coords = [lm.x for lm in hand_landmarks.landmark]
                        y_coords = [lm.y for lm in hand_landmarks.landmark]
                        x_min = int(min(x_coords) * image_width)
                        x_max = int(max(x_coords) * image_width)
                        y_min = int(min(y_coords) * image_height)
                        y_max = int(max(y_coords) * image_height)

                        # Adjust bounding box to square
                        x_min, x_max, y_min, y_max = get_square_bbox(x_min, x_max, y_min, y_max, image_width, image_height)

                        # Crop the image
                        cropped_image = image[y_min:y_max, x_min:x_max]

                        # Save the cropped image in the corresponding label folder
                        output_label_folder = os.path.join(OUTPUT_FOLDER, label)
                        os.makedirs(output_label_folder, exist_ok=True)

                        output_image_path = os.path.join(output_label_folder, f'{file[:-4]}_{handedness}.jpg')
                        cv2.imwrite(output_image_path, cropped_image)

                        # Register the cropped hand
                        if cropped_hand is None:
                            cropped_hand = handedness

                def format_landmarks(landmarks):
                    """Format landmarks as a compact string of (x, y, z) tuples."""
                    if landmarks is None:
                        return "None"
                    return ";".join([f"({lm.x:.4f}, {lm.y:.4f}, {lm.z:.4f})" for lm in landmarks])

                # Process images (include this in the loop where results are processed)
                with open(CSV_FILE, mode='a', newline='') as file_csv:
                    writer = csv.writer(file_csv)
                    writer.writerow([
                        file,  # The image file name
                        hands_found,  # Number of hands found
                        format_landmarks(left_landmarks),  # Left hand landmarks (formatted)
                        format_landmarks(right_landmarks),  # Right hand landmarks (formatted)
                        cropped_hand  # The cropped hand (Left or Right)
                    ])

