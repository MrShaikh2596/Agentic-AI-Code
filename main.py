from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio
from langgraph.graph import StateGraph, START, END
from typing import Optional, TypedDict, Literal
# Call it to load variables from a .env file into os.environ
load_dotenv()


from langchain_tavily import TavilySearch

tool = TavilySearch(
    max_results=5,
    topic="general"
)

# Basic usage


# !pip install -qU langchain langchain-openai langchain-tavily
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

# llm = ChatOllama(
#     #model="qwen3.5:0.8b",
#     model="qwen3.5:2b",
#     temperature=0,
#     # other params...
# )
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
# Initialize the Tavily Search tool
tavily_search = TavilySearch(max_results=5, topic="general")

class agent_state(TypedDict):
    message: str 


def llm_call(state: agent_state):
      response = llm.invoke(state["message"])
      return {"message":response.content}




app =FastAPI()

@app.post("/llm-chat")
async def llm_chat(user_message:str):
    agent_graph = StateGraph(agent_state)
    agent_graph.add_node("llm-call",llm_call)
    agent_graph.add_edge(START,"llm-call")
    agent_graph.add_edge("llm-call",END)
    agent_graph= agent_graph.compile()
    respo = agent_graph.invoke({"message":user_message})
    return respo["message"]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
