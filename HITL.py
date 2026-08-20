from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
import time
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
# from psycopg.rows import dict_row  
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
# llm = ChatOllama(
#     #model="qwen3.5:0.8b",
#     #model="qwen3.5:2b",
#     model = "llama3.2:latest",
#     temperature=0
# )

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def chat_node(state: ChatState):

    decision = interrupt({
        "type": "approval",
        "reason": "Model is about to answer a user question.",
        "question": state["messages"][-1].content,
        "instruction": "Approve this question? yes/no"
    })
    
    if decision["approved"] == 'no':
        return {"messages": [AIMessage(content="Chala JAA Bsdk")]}

    else:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}


# 3. Build the graph: START -> chat -> END
builder = StateGraph(ChatState)

builder.add_node("chat", chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

# Checkpointer is required for interrupts
checkpointer = InMemorySaver()

# Compile the app
app = builder.compile(checkpointer=checkpointer)


# Create a new thread id for this conversation
config = {"configurable": {"thread_id": '1234'}}

# ---- STEP 1: user asks a question ----
initial_input = {
    "messages": [
        ("user", "Capital of India?")
    ]
}

# # Invoke the graph for the first time
result = app.invoke(initial_input, config=config)

print(result)

final_result = app.invoke(
    Command(resume={"approved": "yes"}),
    config=config,
)

print(final_result)