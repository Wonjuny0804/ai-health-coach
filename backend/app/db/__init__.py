"""
Database models and utilities for interacting with Supabase.

This package provides:
- SQL schema definitions
- Pydantic models for chat sessions and messages
- Client functions for interacting with the database
"""

from app.db.models import ChatSession, Message
from app.db.client import (
    get_supabase_client,
    create_chat_session,
    get_chat_session,
    get_user_chat_sessions,
    update_chat_session,
    create_message,
    get_session_messages,
    delete_chat_session
)

__all__ = [
    'ChatSession',
    'Message',
    'get_supabase_client',
    'create_chat_session',
    'get_chat_session',
    'get_user_chat_sessions',
    'update_chat_session',
    'create_message',
    'get_session_messages',
    'delete_chat_session',
]
