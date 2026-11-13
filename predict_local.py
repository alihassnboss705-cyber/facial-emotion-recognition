"""API ke baghair seedha model chalao.
Istemal:  python predict_local.py photo1.jpg photo2.jpg
Har photo ka result print hota hai aur result_<naam>.jpg save hoti hai."""
import os
import sys

import cv2

import core

if len(sys.argv) < 2:
    print("Istemal: python predict_local.py photo.jpg [photo2.jpg ...]")
    sys.exit(1)

for path in sys.argv[1:]:
    img = cv2.imread(path)
    if img is None:
        print(path, "-> image nahi khuli")
        continue
    r = core.predict_image(img)
    print(path, "->", r["label"], r.get("confidence", ""), r.get("reason") or "")
    if r.get("probabilities"):
        top3 = sorted(r["probabilities"].items(), key=lambda kv: -kv[1])[:3]
        print("   ", top3)
    text = r["label"]
    if "confidence" in r:
        text += " " + str(round(r["confidence"] * 100)) + "%"
    cv2.putText(img, text, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                (0, 255, 0), 2)
    out = "result_" + os.path.basename(path)
    cv2.imwrite(out, img)
    print("    saved:", out)
