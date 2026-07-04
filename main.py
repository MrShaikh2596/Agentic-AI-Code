from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import asyncio
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

llm = ChatOllama(
    #model="qwen3.5:0.8b",
    model="qwen3.5:0.8b",
    temperature=0,
    # other params...
)

# Initialize the Tavily Search tool
tavily_search = TavilySearch(max_results=5, topic="general")


async def demo_agent(user_message:str):
#Initialize the agent with the search tool 
    agent = create_agent(
        model=llm,
        tools=[tavily_search],
        system_prompt="You are a helpful research assistant. Use web search to find accurate, up-to-date information."
    )

    # Use the agent
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_message}]
    })
    return response




app =FastAPI()

@app.post("/llm-chat")
async def llm_chat(user_message:str):
    respo = await (demo_agent(user_message))
    return respo["messages"][1].content



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
