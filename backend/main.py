import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from langchain_core.messages import HumanMessage
from backend.api_models import ChatRequest, ChatResponse, EmailRequest

from agents.agent import Agent

app = FastAPI(title="AI Travel Agent API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agent
agent = Agent()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    messages = [HumanMessage(content=request.query)]
    config = {'configurable': {'thread_id': thread_id}}
    
    result = agent.graph.invoke({'messages': messages}, config=config)
    response_content = result['messages'][-1].content
    
    return ChatResponse(response=response_content, thread_id=thread_id)

@app.post("/email")
async def email_endpoint(request: EmailRequest):
    try:
        os.environ['FROM_EMAIL'] = request.sender_email
        os.environ['TO_EMAIL'] = request.receiver_email
        os.environ['EMAIL_SUBJECT'] = request.subject
        
        config = {'configurable': {'thread_id': request.thread_id}}
        
        # Continue the graph execution to run email_sender
        agent.graph.invoke(None, config=config)
        
        return {"status": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
