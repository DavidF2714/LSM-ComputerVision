import cv2
import mediapipe as mp
import os
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

IMAGE_FOLDER = 'LSM.v1i.yolov11/images'

# Collect all image paths from subfolders A-Z
IMAGE_FILES = []
for label_folder in os.listdir(IMAGE_FOLDER):
    label_path = os.path.join(IMAGE_FOLDER, label_folder)
    if os.path.isdir(label_path):
        for image_filename in os.listdir(label_path):
            image_path = os.path.join(label_path, image_filename)
            IMAGE_FILES.append(image_path)

BG_COLOR = (192, 192, 192) # gray
with mp_holistic.Holistic(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    refine_face_landmarks=True) as holistic:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    annotated_image = image.copy()
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    # Check if segmentation_mask exists before using it
    if results.segmentation_mask is not None:
        # Draw segmentation on the image.
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)
    else:
        print(f"Warning: No segmentation mask found for {file}")

    # Draw pose, left and right hands, and face landmarks on the image.
    if results.face_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.
            get_default_pose_landmarks_style())
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.
            get_default_hand_landmarks_style())
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image,
            results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.
            get_default_hand_landmarks_style())
        
    def get_hand_bounding_box(hand_landmarks):
        if hand_landmarks:
            hand_landmarks = [{lm.x, lm.y} for lm in hand_landmarks.landmark]
            min_x = min([point[0] for point in hand_landmarks])
            max_x = max([point[0] for point in hand_landmarks])
            min_y = min([point[1] for point in hand_landmarks])
            max_y = max([point[1] for point in hand_landmarks])
            return int(min_x * image_width), int(min_y * image_height), int(max_x * image_width), int(max_y * image_height)
        return None
    
    left_hand_bbox = get_hand_bounding_box(results.left_hand_landmarks)
    right_hand_bbox = get_hand_bounding_box(results.right_hand_landmarks)
    
    def crop_and_pad_image(bbox):
        if bbox:
            x_min, y_min, x_max, y_max = bbox
            padding = 20    
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(image_width, x_max + padding)
            y_max = min(image_height, y_max + padding)
            cropped_image = image[y_min:y_max, x_min:x_max]
            return cropped_image
        return None
    
    if left_hand_bbox:
        left_hand_cropped = crop_and_pad_image(left_hand_bbox)
        if left_hand_cropped is not None:
            cv2.imwrite(f"left_hand_{idx}.png", left_hand_cropped)