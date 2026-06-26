# Start FastAPI backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python backend/main.py"

# Start Vite frontend
Set-Location frontend
npm run dev
