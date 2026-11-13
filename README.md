# Emotion project (VS Code)

Folder mein ye 2 files bhi rakho (Colab se download hui):
  emotion_final.keras
  emotion_settings.json

Install:        pip install -r requirements.txt
API chalao:     uvicorn main:app --port 8000
Browser:        http://127.0.0.1:8000        (photo upload page)
Docs:           http://127.0.0.1:8000/docs
Bina API:       python predict_local.py photo.jpg
API test:       python test_client.py photo.jpg
Band karna:     Terminal mein Ctrl + C
