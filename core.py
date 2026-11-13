"""Model + face detection + prediction (API aur script dono yahi use karte hain)."""
import json
import os
from pathlib import Path

import cv2
import numpy as np
from tensorflow import keras

BASE = Path(__file__).resolve().parent
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE / "emotion_final.keras"))
CFG_PATH = os.getenv("CFG_PATH", str(BASE / "emotion_settings.json"))

for p in (MODEL_PATH, CFG_PATH):
    if not os.path.exists(p):
        raise FileNotFoundError(
            "Ye file nahi mili: " + p +
            "\nemotion_final.keras aur emotion_settings.json "
            "ko isi folder mein rakho.")



def build_model():
    """Training wala wahi architecture (version masle ka plan B)."""
    from tensorflow.keras import layers
    aug = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.08),
    ])

    def block(x, f, drop):
        x = layers.Conv2D(f, 3, padding="same", activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(f, 3, padding="same", activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D()(x)
        return layers.Dropout(drop)(x)

    inp = keras.Input(shape=(48, 48, 1))
    x = layers.Rescaling(1.0 / 255)(inp)
    x = aug(x)
    x = block(x, 64, 0.2)
    x = block(x, 128, 0.25)
    x = block(x, 256, 0.3)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.4)(x)
    out = layers.Dense(7, activation="softmax")(x)
    return keras.Model(inp, out)


def load_model_safe(path):
    # Plan A: poora model seedha load
    try:
        m = keras.models.load_model(path)
        print(
"Model loaded successfully (directly).")
        return m
    except Exception as e:
        print("Direct loading failed (version mismatch):", str(e)[:120])
    # Plan B: architecture dobara banao aur sirf weights load karo
    m = build_model()
    m.load_weights(path)
    print("Model loaded successfully (architecture + weights).")
    return m


MODEL = load_model_safe(MODEL_PATH)
CFG = json.load(open(CFG_PATH))
CLASS_NAMES = CFG["class_names"]
KEEP = CFG["keep"]
SCALES = np.array(CFG["scales"], dtype="float32")
THRESH = float(CFG["thresh"])
SIZE = int(CFG.get("img_size", 48))
IDX = [CLASS_NAMES.index(c) for c in KEEP]

CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def get_crop(img):
    """Chehra dhoondo (tirchha ho to ghuma kar) aur crop wapas do."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    H, W = gray.shape
    best = None
    for a in [0, -10, 10, -20, 20, -30, 30]:
        M = cv2.getRotationMatrix2D((W / 2, H / 2), a, 1.0)
        g = cv2.warpAffine(
            gray, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
        faces = CASCADE.detectMultiScale(g, 1.1, 4, minSize=(60, 60))
        for (x, y, w, h) in faces:
            if best is None or w * h > best[0]:
                best = (w * h, g, x, y, w, h)
    if best is None:
        return None
    _, g, x, y, w, h = best
    side = int(max(w, h) * 1.4)
    cx, cy = x + w // 2, y + h // 2
    gp = cv2.copyMakeBorder(
        g, side, side, side, side, cv2.BORDER_REPLICATE)
    x0 = cx + side - side // 2
    y0 = cy + side - side // 2
    return gp[y0:y0 + side, x0:x0 + side]


def predict_image(img):
    """img: BGR numpy image. Dict wapas deta hai."""
    crop = get_crop(img)
    if crop is None:
        return {"detected": False, "label": "NO DETECTION",
                "reason": "face nahi mila"}

    f = cv2.resize(crop, (SIZE, SIZE), interpolation=cv2.INTER_AREA)
    batch = np.stack([f, f[:, ::-1]])[..., None].astype("float32")
    pr = MODEL.predict(batch, verbose=0).mean(axis=0) * SCALES
    pr = pr / pr.sum()
    top = int(pr.argmax())

    probs = {c: round(float(p), 4) for c, p in zip(CLASS_NAMES, pr)}
    if top in IDX and pr[top] >= THRESH:
        label, reason = CLASS_NAMES[top].upper(), None
    else:
        label = "NO DETECTION"
        reason = "top emotion: " + CLASS_NAMES[top]
    return {"detected": True, "label": label,
            "confidence": round(float(pr[top]), 4),
            "reason": reason, "probabilities": probs}
