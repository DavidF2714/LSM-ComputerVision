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

    
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
    # Plot pose world landmarks.
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)
    
     # Combine original and annotated images side by side
    combined_image = np.hstack((image, annotated_image))
    
    # Save or display the combined image
    output_path = '/tmp/combined_image_' + str(idx) + '.png'
    cv2.imwrite(output_path, combined_image)
    
    # Display the combined image (optional for testing)
    cv2.imshow('Original and Annotated Image', combined_image)
    cv2.waitKey(0)