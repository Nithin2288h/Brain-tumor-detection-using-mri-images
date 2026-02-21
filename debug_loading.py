import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

print("Libraries imported successfully.")

# Path to the dataset folder
dataset_path = 'dataset/brain-tumor-mri-dataset/'
# Make it absolute to be sure, based on where I run it
# I will run it from c:\Users\bunny\pad project
# So relative path should work if CWD is correct.

# Classes (based on subfolder names)
classes = ['glioma', 'meningioma', 'notumor', 'pituitary']

# Initialize lists for images and labels
images = []
labels = []
image_size = (128, 128)

# Loop through each class folder
for i, class_name in enumerate(classes):
    class_path = os.path.join(dataset_path, class_name)
    if os.path.exists(class_path):
        print(f"Loading images from {class_name}...")
        # Just load one image to verify
        files = os.listdir(class_path)
        if files:
            img_name = files[0]
            img_path = os.path.join(class_path, img_name)
            try:
                img = load_img(img_path, target_size=image_size)
                img_array = img_to_array(img) / 255.0
                images.append(img_array)
                labels.append(i)
                print(f"Successfully loaded {img_path}")
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
                raise e
    else:
        print(f"Folder {class_path} not found.")

print("Test complete.")
