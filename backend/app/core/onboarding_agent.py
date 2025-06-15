from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from app.core.prompt import ONBOARDING_AGENT_PROMPT

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class ResponseFormat(BaseModel):
    """Response format for the agent."""
    result: str


onboarding_agent = create_react_agent(model, tools=[], prompt=ONBOARDING_AGENT_PROMPT, response_format=ResponseFormat)