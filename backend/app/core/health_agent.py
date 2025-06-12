from typing import Annotated, Sequence, TypedDict, Any
from operator import add as add_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from app.core.supabase import supabase

# Import locally for CLI version
try:
    from utils import print_custom_banner
except ImportError:
    def print_custom_banner():
        print("=== AI HEALTH COACH ===")

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class AgentState(TypedDict):
    context: dict[str, Any]
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

    # check if the last message is exit_conversation
    last_message = messages[-1]
    if isinstance(last_message, HumanMessage) and "exit_conversation" in last_message.content.lower():
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
            print(f"\n🤖 Agent: {message.content}")
        elif isinstance(message, HumanMessage):
            print(f"\n👤 User: {message.content}")

def save_history(messages, filename="history.txt"):
    with open(filename, "w") as f:
        for message in messages:
            if isinstance(message, AIMessage):
                f.write(f"Agent: {message.content}\n")
            elif isinstance(message, HumanMessage):
                f.write(f"User: {message.content}\n")

def load_history(filename="history.txt"):
    messages = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Agent: "):
                    messages.append(AIMessage(content=line[len("Agent: "):]))
                elif line.startswith("User: "):
                    messages.append(HumanMessage(content=line[len("User: "):]))
        return messages
    except FileNotFoundError:
        return []


def run_agent():
    print_custom_banner()
    # load chat history.
    messages = load_history()
    state = {"messages": messages}

    for step in agent.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
            save_history(step["messages"])

    print("\n === HEALTH COACH AGENT FINISHED ===")

if __name__ == "__main__":
    run_agent()
