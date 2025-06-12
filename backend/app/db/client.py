import os
from typing import Dict, List, Any, Optional
import uuid
from supabase import create_client, Client
from datetime import datetime

from app.db.models import ChatSession, Message

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Get or create Supabase client"""
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

# Chat Sessions operations
async def create_chat_session(user_id: uuid.UUID, title: str, metadata: Optional[Dict[str, Any]] = None) -> ChatSession:
    """Create a new chat session"""
    supabase = get_supabase_client()
    
    session_data = {
        "user_id": str(user_id),
        "title": title,
        "created_at": datetime.now().isoformat(),
        "last_activity_at": datetime.now().isoformat()
    }
    
    result = supabase.table("chat_sessions").insert(session_data).execute()
    
    if len(result.data) > 0:
        return ChatSession(**result.data[0])
    raise Exception("Failed to create chat session")

async def get_chat_session(session_id: uuid.UUID) -> ChatSession:
    """Get chat session by id"""
    supabase = get_supabase_client()
    
    result = supabase.table("chat_sessions").select("*").eq("id", str(session_id)).execute()
    
    if len(result.data) > 0:
        return ChatSession(**result.data[0])
    raise Exception(f"Chat session with id {session_id} not found")

async def get_user_chat_sessions(user_id: uuid.UUID) -> List[ChatSession]:
    """Get all chat sessions for a user"""
    supabase = get_supabase_client()
    
    result = supabase.table("chat_sessions") \
        .select("*") \
        .eq("user_id", str(user_id)) \
        .order("created_at", desc=True) \
        .execute()
    
    return [ChatSession(**session) for session in result.data]

async def update_chat_session(session_id: uuid.UUID, updates: Dict[str, Any]) -> ChatSession:
    """Update a chat session"""
    supabase = get_supabase_client()
    
    updates["last_activity_at"] = datetime.now().isoformat()
    
    result = supabase.table("chat_sessions") \
        .update(updates) \
        .eq("id", str(session_id)) \
        .execute()
    
    if len(result.data) > 0:
        return ChatSession(**result.data[0])
    raise Exception(f"Failed to update chat session with id {session_id}")

# Messages operations
async def create_message(session_id: uuid.UUID, role: str, content: str) -> Message:
    """Create a new message"""
    supabase = get_supabase_client()
    
    # Validate role to match database constraint
    if role not in ['user', 'assistant']:
        raise ValueError("Role must be either 'user' or 'assistant'")
        
    message_data = {
        "session_id": str(session_id),
        "role": role,
        "content": content,
        "created_at": datetime.now().isoformat()
    }
    
    result = supabase.table("messages").insert(message_data).execute()
    
    if len(result.data) > 0:
        return Message(**result.data[0])
    raise Exception("Failed to create message")

async def get_session_messages(session_id: uuid.UUID) -> List[Message]:
    """Get all messages for a chat session"""
    supabase = get_supabase_client()
    
    result = supabase.table("messages") \
        .select("*") \
        .eq("session_id", str(session_id)) \
        .order("created_at") \
        .execute()
    
    return [Message(**message) for message in result.data]

async def delete_chat_session(session_id: uuid.UUID) -> bool:
    """Delete a chat session (and associated messages via CASCADE)"""
    supabase = get_supabase_client()
    
    result = supabase.table("chat_sessions") \
        .delete() \
        .eq("id", str(session_id)) \
        .execute()
    
    return len(result.data) > 0
