import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)

# Path to the trained model (one level up from webapp/)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'brain_tumor_detector.h5')

# Class labels — must match training order in model.ipynb
CLASS_LABELS = ['glioma', 'meningioma', 'notumor', 'pituitary']
CLASS_DISPLAY = {
    'glioma':     'Glioma',
    'meningioma': 'Meningioma',
    'notumor':    'No Tumor',
    'pituitary':  'Pituitary',
}

# Image size used during training
IMG_SIZE = (128, 128)

# Load model once at startup
import urllib.request

print("Loading model...")
if not os.path.exists(MODEL_PATH):
    # Check if a model download URL is set in environment variables (for serverless environments)
    download_url = os.environ.get('MODEL_DOWNLOAD_URL')
    if download_url:
        print(f"Model file not found. Downloading from {download_url}...")
        tmp_model_path = '/tmp/brain_tumor_detector.h5'
        if not os.path.exists(tmp_model_path):
            urllib.request.urlretrieve(download_url, tmp_model_path)
            print("Model downloaded successfully!")
        MODEL_PATH = tmp_model_path
    else:
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Please upload the model or set the 'MODEL_DOWNLOAD_URL' environment variable in your deployment settings."
        )

model = load_model(MODEL_PATH)
print("Model loaded successfully!")


def preprocess_image(image_bytes):
    """Convert uploaded image bytes to model-ready numpy array."""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        image_bytes = file.read()
        img_array = preprocess_image(image_bytes)

        predictions = model.predict(img_array)[0]          # shape: (4,)
        pred_idx = int(np.argmax(predictions))
        raw_label = CLASS_LABELS[pred_idx]
        predicted_class = CLASS_DISPLAY[raw_label]
        confidence = float(predictions[pred_idx]) * 100

        all_scores = {
            CLASS_DISPLAY[CLASS_LABELS[i]]: float(predictions[i]) * 100
            for i in range(len(CLASS_LABELS))
        }

        is_tumor = raw_label != 'notumor'

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence,
            'is_tumor': is_tumor,
            'all_scores': all_scores
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
