from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional 
from app.core.onboarding_agent import onboarding_agent

router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
    responses={404: {"description": "Not found"}},
)

class ChatMessage(BaseModel):
    content: str
    role: str = "user"  # "user" or "assistant"

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    data: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Endpoint for handling onboarding chat interactions.
    
    This endpoint receives messages from the user during the onboarding process
    and returns appropriate responses based on the conversation context.
    """
    
    # when message comes in, for every user, there'd be only one onboarding converstion history that's needed.
    # so we need to load the conversation history that matches the user_id from the database and pass it to the agent.
    
    response = onboarding_agent.invoke({ "messages": [{"role": "user", "content": request.message}]})
    print(f"Response: {response['messages'][-1].content}")
    
    return ChatResponse(
        data=response['messages'][-1].content,
    )
