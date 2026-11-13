"""FastAPI server. Chalao:  uvicorn main:app --port 8000"""
import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

import core

MAX_BYTES = 5 * 1024 * 1024  # 5 MB

app = FastAPI(title="Emotion API", version="1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"])

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Emotion Detector</title>
<style>
body{font-family:Arial,sans-serif;max-width:560px;margin:30px auto;padding:0 14px}
#out{margin-top:16px}
.big{font-size:28px;font-weight:bold}
.ok{color:#1a7f37}.no{color:#c62828}
.row{display:flex;align-items:center;margin:4px 0;font-size:14px}
.row span{width:80px}
.bar{background:#1f77b4;height:14px;border-radius:3px}
img{max-width:100%;margin-top:10px;border-radius:6px}
</style></head><body>
<h2>Emotion Detector</h2>
<p>Angry, sad, happy ya neutral. Baaqi par NO DETECTION.</p>
<input type="file" id="f" accept="image/*">
<button onclick="go()">Check karo</button>
<div id="out"></div>
<script>
async function go(){
  const f=document.getElementById("f").files[0];
  const out=document.getElementById("out");
  if(!f){out.textContent="Pehle photo chuno";return;}
  out.textContent="Soch raha hoon...";
  const fd=new FormData();fd.append("file",f);
  const r=await fetch("/predict",{method:"POST",body:fd});
  const d=await r.json();
  if(!r.ok){out.textContent=d.detail||"Error";return;}
  let h='<div class="big '+(d.label==="NO DETECTION"?"no":"ok")+'">'+d.label+'</div>';
  if(d.confidence!==undefined){h+='<div>Yaqeen: '+(d.confidence*100).toFixed(1)+'%</div>';}
  if(d.reason){h+='<div>'+d.reason+'</div>';}
  if(d.probabilities){
    for(const k in d.probabilities){
      const p=d.probabilities[k]*100;
      h+='<div class="row"><span>'+k+'</span><div class="bar" style="width:'+p*3+'px"></div>&nbsp;'+p.toFixed(1)+'%</div>';
    }
  }
  h+='<img src="'+URL.createObjectURL(f)+'">';
  out.innerHTML=h;
}
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE


@app.get("/health")
def health():
    return {"status": "ok", "classes": core.CLASS_NAMES,
            "shown": core.KEEP}


@app.post("/predict")
def predict(file: UploadFile = File(...)):
    data = file.file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "The file is larger than 5 MB.")
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "This is not a valid image.")
    return core.predict_image(img)
