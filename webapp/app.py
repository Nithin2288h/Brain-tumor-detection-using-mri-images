import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# ── Rebuild model architecture (same as notebook) and load weights ──
# This bypasses Keras version serialization issues
def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(4, activation='softmax')
    ])
    return model

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'brain_tumor_detector.h5')
model = build_model()
model.load_weights(MODEL_PATH)
print("Model weights loaded successfully!")

CLASS_LABELS = ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary']
IMAGE_SIZE = (128, 128)


def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(IMAGE_SIZE)
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


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

        predictions = model.predict(img_array, verbose=0)[0]
        predicted_index = int(np.argmax(predictions))
        confidence = float(np.max(predictions)) * 100
        predicted_label = CLASS_LABELS[predicted_index]

        all_scores = {
            CLASS_LABELS[i]: round(float(predictions[i]) * 100, 2)
            for i in range(len(CLASS_LABELS))
        }

        return jsonify({
            'predicted_class': predicted_label,
            'confidence': round(confidence, 2),
            'is_tumor': predicted_label != 'No Tumor',
            'all_scores': all_scores
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
