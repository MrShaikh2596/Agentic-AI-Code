from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Any, Annotated, Optional, TypedDict, Literal
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from tools import search_tool, calculator, get_stock_price
from langgraph.prebuilt import ToolNode, tools_condition
import io
from PIL import Image as PILImage


# Call it to load variables from a .env file into os.environ
load_dotenv()

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

tools = [get_stock_price, calculator]


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)


class agent_state(TypedDict):
    messages: Annotated[list[Any], add_messages]


def llm_call(state: agent_state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

app =FastAPI()

@app.post("/llm-chat")
async def llm_chat(user_message:str):
    agent_graph = StateGraph(agent_state) 
    agent_graph.add_node("llm-call",llm_call)
    agent_graph.add_node("tools",ToolNode(tools=tools))
    agent_graph.add_edge(START,"llm-call")
    agent_graph.add_conditional_edges( "llm-call",tools_condition)
    agent_graph.add_edge("tools","llm-call")
    agent_graph= agent_graph.compile()
    # with open("graph.png", "wb") as f:
    #     f.write(agent_graph.get_graph().draw_mermaid_png())
    async def response_generator():
        async for chunk, metadata in agent_graph.astream({"messages": [HumanMessage(content=user_message)]}, stream_mode="messages"):
            # Only stream the LLM's final answer: skip tool-call chunks and empty content
            if metadata.get("langgraph_node") == "llm-call" and not getattr(chunk, "tool_call_chunks", None) and chunk.content:
                yield chunk.content
    return StreamingResponse(response_generator(), media_type="text/plain")
   #return agent_graph.invoke({"messages": [user_message]})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# agent_graph = StateGraph(agent_state) 
# agent_graph.add_node("llm-call",llm_call)
# agent_graph.add_node("tools",ToolNode(tools=tools))
# agent_graph.add_edge(START,"llm-call")

# # agent_graph.add_edge("llm-call",END)
# agent_graph= agent_graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(agent_graph.get_graph().draw_mermaid_png())

