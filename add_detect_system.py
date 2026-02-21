import json

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

detect_cell_source = [
    "%matplotlib inline\n",
    "from tensorflow.keras.preprocessing.image import load_img, img_to_array\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Class labels (must match training order)\n",
    "class_labels = ['glioma', 'meningioma', 'notumor', 'pituitary']\n",
    "\n",
    "def detect_and_display(img_path, model, image_size=128):\n",
    "    \"\"\"\n",
    "    Detects brain tumor from an MRI image and displays the result.\n",
    "    - Shows 'No Tumor' if notumor class is predicted.\n",
    "    - Otherwise shows the tumor type and confidence score.\n",
    "    \"\"\"\n",
    "    try:\n",
    "        # Load and preprocess the image\n",
    "        img = load_img(img_path, target_size=(image_size, image_size))\n",
    "        img_array = img_to_array(img) / 255.0\n",
    "        img_batch = np.expand_dims(img_array, axis=0)\n",
    "\n",
    "        # Predict\n",
    "        predictions = model.predict(img_batch, verbose=0)\n",
    "        predicted_index = np.argmax(predictions, axis=1)[0]\n",
    "        confidence = np.max(predictions, axis=1)[0] * 100\n",
    "\n",
    "        # Determine result label\n",
    "        predicted_label = class_labels[predicted_index]\n",
    "        if predicted_label == 'notumor':\n",
    "            result = 'No Tumor Detected'\n",
    "            color = 'green'\n",
    "        else:\n",
    "            result = f'Tumor Detected: {predicted_label.capitalize()}'\n",
    "            color = 'red'\n",
    "\n",
    "        # Display\n",
    "        plt.figure(figsize=(5, 5))\n",
    "        plt.imshow(load_img(img_path))\n",
    "        plt.axis('off')\n",
    "        plt.title(f'{result}\\nConfidence: {confidence:.2f}%',\n",
    "                  fontsize=13, color=color, fontweight='bold')\n",
    "        plt.tight_layout()\n",
    "        plt.show()\n",
    "\n",
    "        print(f'Result     : {result}')\n",
    "        print(f'Confidence : {confidence:.2f}%')\n",
    "        print(f'All Scores : { {class_labels[i]: f\"{predictions[0][i]*100:.2f}%\" for i in range(len(class_labels))} }')\n",
    "\n",
    "    except Exception as e:\n",
    "        print('Error processing the image:', str(e))\n",
    "\n",
    "print('detect_and_display() function is ready!')\n",
    "print('Usage: detect_and_display(\"path/to/mri_image.jpg\", model)')\n",
    "\n",
    "# ── Test on a sample from the test set ──\n",
    "# Uncomment and replace with a real image path to test:\n",
    "# detect_and_display('dataset/brain-tumor-mri-dataset/glioma/your_image.jpg', model)\n"
]

detect_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": detect_cell_source
}

nb['cells'].append(detect_cell)

with open('model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Tumor Detection System cell added successfully.")
