-- Schema definitions for Supabase database

-- Chat Sessions Table
CREATE TABLE IF NOT EXISTS "chat_sessions" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title TEXT NOT NULL DEFAULT 'New Chat',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Create index on user_id for faster querying sessions by user
CREATE INDEX IF NOT EXISTS chat_sessions_user_id_idx ON "chat_sessions" (user_id);

-- Messages Table
CREATE TABLE IF NOT EXISTS "messages" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES "chat_sessions" (id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role = ANY (ARRAY['user'::text, 'assistant'::text])),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Create index on session_id for faster querying messages by session
CREATE INDEX IF NOT EXISTS messages_session_id_idx ON "messages" (session_id);

-- Add RLS (Row Level Security) policies
ALTER TABLE "chat_sessions" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "messages" ENABLE ROW LEVEL SECURITY;

-- Policy for chat_sessions (users can only see their own sessions)
CREATE POLICY "Users can view own sessions" ON "chat_sessions"
FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" ON "chat_sessions"
FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions" ON "chat_sessions"
FOR UPDATE
USING (auth.uid() = user_id);

-- Policy for messages (users can only see messages from their sessions)
CREATE POLICY "Users can view messages from own sessions" ON "messages"
FOR SELECT
USING (
  session_id IN (
    SELECT id FROM chat_sessions WHERE user_id = auth.uid()
  )
);

CREATE POLICY "Users can insert messages to own sessions" ON "messages"
FOR INSERT
WITH CHECK (
  session_id IN (
    SELECT id FROM chat_sessions WHERE user_id = auth.uid()
  )
);
