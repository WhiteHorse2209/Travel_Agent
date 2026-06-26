# 🌍 AI Travel Agent V2

A modern, "Future One" premium AI Travel Assistant that provides a rich conversational interface for finding flights, hotels, and weather forecasts.

Built with a completely decoupled architecture, this agent leverages LangGraph's advanced tool-calling and memory checkpointing alongside a gorgeous React frontend. 

---

## ✨ Features
- ✈️ **Flight Search**: Real-time Google Flights lookup via SerpApi.
- 🏨 **Hotel Search**: Real-time Google Hotels lookup via SerpApi.
- ⛅ **Weather Forecast**: Accurate 7-day weather predictions using Open-Meteo.
- ✉️ **Automated Email Itineraries**: Dynamically generates HTML itineraries and sends them directly to your inbox via SendGrid.
- 💬 **Interactive Chat**: A sleek React chat interface featuring glassmorphism, dynamic gradients, and animated markdown rendering.

---

## 🏗️ Architecture Stack
- **Backend:** Python + FastAPI + LangChain/LangGraph + Groq (LLaMA 3)
- **Frontend:** Vite + React + Vanilla CSS (Glassmorphism & Gradients) + React Markdown

---

## 🚀 Setup Instructions

### 1. Configure your Environment
You must keep your API keys in a `.env` file in the root directory. **Do not share this file publicly.**
Create a file named `.env` and add the following:

```env
GROQ_API_KEY="your_groq_key_here"
SERPAPI_API_KEY="your_serpapi_key_here"
SENDGRID_API_KEY="your_sendgrid_key_here"
FROM_EMAIL="your_verified_sendgrid_email@example.com"
```
*(Note: The Weather tool uses Open-Meteo which is completely free and requires no API key!)*

### 2. Install Backend Dependencies
Open a terminal in the root directory and install the required Python packages:
```bash
pip install fastapi uvicorn pydantic python-dotenv langchain langchain-openai langchain-groq langgraph sendgrid serpapi google-search-results
```

### 3. Install Frontend Dependencies
Navigate to the `frontend` folder and install the Node packages:
```bash
cd frontend
npm install
```

### 4. Run the Application
You can start both the backend and frontend simultaneously using the provided script:
```bash
.\run.ps1
```
Open your browser to `http://localhost:5173` and start planning your perfect trip!

---

## 🛠️ Challenges & How We Solved Them

Throughout the development of this AI agent, we encountered several fascinating edge cases and API quirks. Here is a summary of the mistakes and how we engineered solutions for them:

### 1. Groq LLaMA 3 Tool Calling Crashes (400 Bad Request)
**The Problem:** When searching for flights and hotels, the SerpApi Google engine returned massive JSON payloads (including hundreds of hidden metadata fields like CO2 emissions, layovers, and dozens of thumbnail URLs). The LLM tried to pass all of this data as a single markdown string to the `send_email` tool. This massive string exceeded Groq's parser limits, causing the LLM to hallucinate the tool call payload directly into the function name, resulting in a `400 BadRequest tool call validation failed`.
**The Solution:** We decoupled the content generation from the LLM tool schema. We removed the `content` parameter from the `send_email` tool, meaning the LLM only needed to output `to_email` and `subject`. Then, inside `agent.py`, we dynamically intercepted the tool call and injected the conversation history directly into the email logic in the backend. We also aggressively filtered the raw SerpApi JSON down to just the essential fields (price, name, duration, and one image).

### 2. SendGrid Silently Dropping Emails (202 Accepted but no email)
**The Problem:** We implemented SendGrid, and the backend logged a successful `202 Accepted` status code. However, the emails never arrived in the inbox. 
**The Solution:** SendGrid immediately returns a 202 status asynchronously, but drops the email behind the scenes if the `FROM_EMAIL` address isn't verified in the SendGrid Dashboard to comply with CAN-SPAM laws. We solved this by walking through the Single Sender Verification process, providing a physical address on the SendGrid dashboard, and ensuring the `FROM_EMAIL` in the `.env` perfectly matched the verified sender.

### 3. Pydantic Validation Errors on Flights
**The Problem:** The `flights_finder.py` tool crashed when the user asked for a one-way flight because the `return_date` field was missing, triggering a Pydantic `Field required` error.
**The Solution:** We updated the `FlightsInput` Pydantic model to make `return_date` optional (`Optional[str] = Field(default=None)`), allowing the LLM to dynamically search for one-way flights without crashing the backend.

### 4. Context Awareness (Relative Dates)
**The Problem:** When asked to find flights for "tomorrow," the LLM had no frame of reference and defaulted to an example date found in its tool schema (e.g. 2024). 
**The Solution:** Instead of hardcoding a static year, we injected `datetime.datetime.now().strftime("%A, %B %d, %Y")` directly into the `TOOLS_SYSTEM_PROMPT` during the `call_tools_llm` node execution. This gave the LLM perfect real-time awareness of the exact current date, allowing it to seamlessly resolve relative terms like "today," "tomorrow," and "next Tuesday."

---
*Built with ❤️ for the future of AI travel planning.*
