#!/bin/bash
cd "$(dirname "$0")"

source .venv/bin/activate

uvicorn backend:app --port 8000 &
BACKEND_PID=$!

cd frontend
npm run dev -- --host 127.0.0.1 &
FRONTEND_PID=$!

sleep 4
open http://localhost:5173

trap 'kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait
