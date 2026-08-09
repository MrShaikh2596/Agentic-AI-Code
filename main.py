from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio
import logging
import os
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Any, Annotated, Optional, TypedDict, Literal
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition
import io
from PIL import Image as PILImage
from langchain_mcp_adapters.client import MultiServerMCPClient



# Call it to load variables from a .env file into os.environ
load_dotenv()

# Basic usage


# !pip install -qU langchain langchain-openai langchain-tavily
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

# llm = ChatOllama(
#     #model="qwen3.5:0.8b",
#     model="qwen3.5:2b",
#     temperature=0,
#     # other params...
# )

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_TEAM_ID = os.getenv("SLACK_TEAM_ID")
DEBUG_CHECKPOINTER = os.getenv("DEBUG_CHECKPOINTER", "1").lower() in {"1", "true", "yes", "on"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("checkpointer_debug")
logger.setLevel(logging.DEBUG)


def log_checkpointer_state(label: str, graph: Any, checkpointer: Any, config: dict[str, Any]) -> None:
    if not DEBUG_CHECKPOINTER:
        return

    logger.debug("%s checkpointer: %s", label, checkpointer)
    logger.debug("%s config: %s", label, config)

    state_method = getattr(graph, "get_state", None)
    if callable(state_method):
        try:
            state_value = state_method(config)
            logger.debug("%s state via graph.get_state: %s", label, state_value)
        except Exception as exc:
            logger.debug("%s graph.get_state failed: %s", label, exc)
    else:
        logger.debug("%s graph.get_state is unavailable for this graph", label)

    history_method = getattr(graph, "get_state_history", None)
    if callable(history_method):
        try:
            history_value = history_method(config)
            logger.debug("%s history via graph.get_state_history: %s", label, history_value)
        except Exception as exc:
            logger.debug("%s graph.get_state_history failed: %s", label, exc)
    else:
        logger.debug("%s graph.get_state_history is unavailable for this graph", label)


client = MultiServerMCPClient(
    {
        "AgenticAI Tools Server": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8200/mcp",
        },
        "slack": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-slack"],
                        "transport": "stdio",
                        "env": {
                            "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN,
                            "SLACK_TEAM_ID": SLACK_TEAM_ID,
                        },
                    }
    }
            
)





llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)



class agent_state(TypedDict):
    messages: Annotated[list[Any], add_messages]


app = FastAPI()

@app.post("/llm-chat")
async def llm_chat(user_message: str):
    async def response_generator():
        # Aggregate tools from ALL configured MCP servers (AgenticAI Tools Server + slack).
        # get_tools() manages its own sessions per server, so no manual client.session() is needed.
        tools = await client.get_tools()

        # per-request llm_call captures the live `tools`
        async def llm_call_local(state: agent_state):
            llm_with_tools = llm.bind_tools(tools)
            response = await llm_with_tools.ainvoke(state["messages"])
            return {"messages": [response]}

        agent_graph = StateGraph(agent_state)
        agent_graph.add_node("llm-call", llm_call_local)
        agent_graph.add_node("tools", ToolNode(tools=tools))
        agent_graph.add_edge(START, "llm-call")
        agent_graph.add_conditional_edges("llm-call", tools_condition)
        agent_graph.add_edge("tools", "llm-call")
        checkpointer = InMemorySaver()
        agent_graph = agent_graph.compile(checkpointer=checkpointer)
        config1 = {"configurable": {"thread_id": "1"}}
        log_checkpointer_state("before-invocation", agent_graph, checkpointer, config1)

        async for chunk, metadata in agent_graph.astream(
            {"messages": [HumanMessage(content=user_message)]},
            stream_mode="messages",
            config=config1

        ):
            # Only stream the LLM's final answer: skip tool-call chunks and empty content
            if (
                metadata.get("langgraph_node") == "llm-call"
                and not getattr(chunk, "tool_call_chunks", None)
                and chunk.content
            ):
                yield chunk.content

        log_checkpointer_state("after-invocation", agent_graph, checkpointer, config1)

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

