# AI Travel Agent V2

A modern, "Future One" premium AI Travel Assistant that provides a rich conversational interface for finding flights, hotels, and weather forecasts.

This project uses a decoupled architecture:
- **Backend:** Python + FastAPI + LangChain/LangGraph
- **Frontend:** Vite + React + Vanilla CSS (Glassmorphism & Gradients)

## Features
- ✈️ **Flight Search**: Real-time Google Flights lookup via SerpApi.
- 🏨 **Hotel Search**: Real-time Google Hotels lookup via SerpApi.
- ⛅ **Weather Forecast**: Accurate 7-day weather predictions using Open-Meteo.
- 💬 **Interactive Chat**: A sleek React chat interface for iterative travel planning.

## Prerequisites
- Python 3.11+
- Node.js 18+
- API Keys for OpenAI and SerpApi (See Setup section).

## Getting API Keys

You must keep your API keys in a `.env` file in the root directory. **Do not share this file publicly.**

1. **Groq API Key**
   - Get it from: [https://console.groq.com/keys](https://console.groq.com/keys)
   - *Why do we need it?* It powers the core AI "brain" of the agent using lightning-fast LLaMA 3.

2. **SerpApi API Key**
   - Get it from: [https://serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)
   - *Why do we need it?* It connects the AI to real-time Google Flights and Hotels data.

3. **SendGrid API Key (Optional)**
   - Get it from: [https://app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys)
   - *Why do we need it?* Only required if you want to use the agent's email itinerary feature.

*(Note: The Weather tool uses Open-Meteo which is completely free and requires no API key!)*

## Setup Instructions

### 1. Configure your Environment
Copy the example environment file and add your keys:
1. Rename `.env.example` to `.env`
2. Open `.env` and fill in your keys (e.g., `GROQ_API_KEY="gsk_..."`).

### 2. Install Backend Dependencies
Open a terminal in the root directory and install the required Python packages:
```bash
pip install fastapi uvicorn pydantic python-dotenv langchain langchain-openai langgraph sendgrid serpapi
```

### 3. Install Frontend Dependencies
Navigate to the `frontend` folder and install the Node packages:
```bash
cd frontend
npm install
```

## Running the Application

You can start both the backend and frontend at the same time using the provided PowerShell script:

```bash
.\run.ps1
```

Alternatively, you can run them manually in separate terminal windows:

**Terminal 1 (Backend):**
```bash
python backend/main.py
```
*(The backend runs on http://localhost:8000)*

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
*(The frontend runs on http://localhost:5173)*

Open your browser to `http://localhost:5173` and start planning your perfect trip!
