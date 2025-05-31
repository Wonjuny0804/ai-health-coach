from typing import Annotated, Sequence, TypedDict
from operator import add as add_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def agent_node(state: AgentState) -> AgentState:
    """ This is the agent node. It takes in a state and returns a new state."""
    system_prompt = SystemMessage(content="""
    You are a helpful health coach assistant. Users will ask you questions about their health and fitness.
    You will answer their questions in a helpful and concise way. 

    - Always try to know what is their main goal for a workout before giving a workout plan.
    - If user asks about a specific workout, try to give a workout plan that matches their goal.
    - If user asks about a diet plan, try to give a diet plan that matches their goal.
    - Always stick to the topic of the conversation which is health and fitness, if user asks about something else, try to redirect the conversation to health and fitness.
    - To end the conversation, user can say "exit_conversation".
    """)
    
    if not state["messages"]:
        user_input = "I am ready to help you with your health, How can I help you?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\nHow would you like me to help you? ")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = llm.invoke(all_messages)
    
    
    return {"messages": list(state["messages"]) + [user_message,response]}
    

def should_continue(state: AgentState) -> str:
    """ This function decides whether to continue the conversation or not,"""
    messages = state["messages"]
    
    if not messages:
        return "continue"

    for message in reversed(messages):
        if (isinstance(message, HumanMessage) and "exit_conversation" in message.content.lower()):
            return "end"

    return "continue"

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)


graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {
    "continue": "agent",
    "end": END
})
agent = graph.compile()


def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return

    for message in messages[-3:]:
        if isinstance(message, AIMessage):
            print(f"\nAssistant: {message.content}")
        elif isinstance(message, HumanMessage):
            print(f"\nUser: {message.content}")


def run_agent():
    print("\n === HEALTH COACH AGENT ===")

    state = {"messages": []}

    for step in agent.stream(state, stream_mode="values"):
        if "messages" in step:
            # print(step["messages"])
            print_messages(step["messages"])

    print("\n === HEALTH COACH AGENT FINISHED ===")

if __name__ == "__main__":
    run_agent()