import json

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

save_load_cell_source = [
    "# ── Save & Load Model for Future Brain Tumor Detection ──\n",
    "from tensorflow.keras.models import load_model\n",
    "import numpy as np\n",
    "import cv2\n",
    "\n",
    "# ── SAVE ──\n",
    "model.save('brain_tumor_detector.h5')\n",
    "print('Model saved as brain_tumor_detector.h5')\n",
    "\n",
    "# ── LOAD ──\n",
    "loaded_model = load_model('brain_tumor_detector.h5')\n",
    "print('Model loaded successfully!')\n",
    "loaded_model.summary()\n",
    "\n",
    "# ── PREDICT on a New MRI Image ──\n",
    "def predict_tumor(image_path, model, classes, image_size=(128, 128)):\n",
    "    img = cv2.imread(image_path)\n",
    "    img = cv2.resize(img, image_size)\n",
    "    img = img / 255.0\n",
    "    img = np.expand_dims(img, axis=0)  # Add batch dimension\n",
    "    predictions = model.predict(img)\n",
    "    predicted_class = classes[np.argmax(predictions)]\n",
    "    confidence = np.max(predictions) * 100\n",
    "    print(f'Predicted Class : {predicted_class}')\n",
    "    print(f'Confidence      : {confidence:.2f}%')\n",
    "    return predicted_class, confidence\n",
    "\n",
    "# ── Example Usage ──\n",
    "# Replace 'path/to/your/mri_image.jpg' with an actual image path\n",
    "# predicted_class, confidence = predict_tumor('path/to/your/mri_image.jpg', loaded_model, classes)\n",
    "print('\\nTo predict a new MRI image, call:')\n",
    "print(\"  predict_tumor('path/to/mri.jpg', loaded_model, classes)\")\n"
]

save_load_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": save_load_cell_source
}

nb['cells'].append(save_load_cell)

with open('model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Save & Load Model cell added successfully.")
