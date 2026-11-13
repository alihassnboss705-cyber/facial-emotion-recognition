# Facial Emotion Recognition System

An AI-powered Facial Emotion Recognition System built using a Convolutional Neural Network (CNN), TensorFlow, FastAPI, and React.

The application detects a face in an uploaded image and predicts its facial emotion. It supports four final emotion outputs: **Angry, Happy, Sad, and Neutral**. Unsupported emotions or predictions below the configured confidence threshold return **NO DETECTION**.

## Features

- CNN-based facial emotion recognition
- Seven-class emotion prediction
- Face detection using OpenCV Haar Cascade
- Face cropping and image preprocessing
- 48×48 grayscale input images
- Horizontal flip test-time augmentation
- Confidence score and emotion probabilities
- React-based user interface
- FastAPI backend
- Maximum image upload size: 5 MB
- Health-check API endpoint

## Emotions

The CNN model predicts seven emotions:

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Surprise

The application displays four supported emotions:

- Angry
- Happy
- Sad
- Neutral

Other predictions return `NO DETECTION`.

## CNN Architecture

The model uses a Convolutional Neural Network (CNN).

The architecture includes:

1. Input layer: 48×48 grayscale image
2. Rescaling layer
3. Data augmentation
4. Convolutional blocks with 64, 128, and 256 filters
5. Batch Normalization
6. ReLU activation
7. Max Pooling
8. Dropout layers
9. Global Average Pooling
10. Dense layer with 256 neurons
11. Softmax output layer with 7 classes

## Tech Stack

**Machine Learning**
- Python
- TensorFlow / Keras
- CNN
- NumPy
- OpenCV

**Backend**
- FastAPI
- Uvicorn
- Python

**Frontend**
- React
- Vite
- JavaScript
- CSS

## Project Structure

```text
emotion_project/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── App.css
│
├── backend.py
├── core.py
├── emotion_final.keras
├── emotion_settings.json
├── predict_local.py
├── test_client.py
├── requirements.txt
├── requirements-intel-mac.txt
├── run.sh
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:alihassnboss705-cyber/facial-emotion-recognition.git
cd facial-emotion-recognition
```

### 2. Create Python Virtual Environment

Python 3.11 is specified for this project.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

## Run the Application

Make sure the virtual environment is activated and frontend dependencies are installed.

```bash
chmod +x run.sh
./run.sh
```

Open the frontend:

http://localhost:5173

Backend API:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Press `Ctrl + C` in the terminal to stop the application.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Basic HTML emotion detector |
| GET | `/health` | Backend health check |
| POST | `/predict` | Predict emotion from uploaded image |

### Prediction API

Send an image using multipart form-data.

Field name:

```text
file
```

Example response:

```json
{
  "detected": true,
  "label": "HAPPY",
  "confidence": 0.91,
  "reason": null,
  "probabilities": {
    "angry": 0.02,
    "disgust": 0.01,
    "fear": 0.01,
    "happy": 0.91,
    "neutral": 0.02,
    "sad": 0.02,
    "surprise": 0.01
  }
}
```

*Example response only. Actual predictions and confidence scores depend on the uploaded image.*

## Model Files

The following files are required:

- `emotion_final.keras` — Trained CNN model.
- `emotion_settings.json` — Model configuration, class names, supported labels, and prediction settings.

Both files should be present in the project root directory.

## Local Prediction

You can also use the prediction script without the React frontend:

```bash
python predict_local.py image.jpg
```

## Future Improvements

- Improve model accuracy and generalization.
- Add real-time webcam emotion detection.
- Improve face detection under different lighting conditions.
- Deploy the application to a cloud platform.

## Author

**Ali Hassan**

GitHub: https://github.com/alihassnboss705-cyber

---

**Facial Emotion Recognition System — Powered by CNN, TensorFlow, FastAPI, and React.**
