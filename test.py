from dotenv import load_dotenv
# Call it to load variables from a .env file into os.environ
load_dotenv()

from langchain_tavily import TavilySearch

tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # start_date=None,
    # end_date=None,
    # include_domains=None,
    # exclude_domains=None,
    # include_usage= False
)

# Basic usage
# result = tool.invoke({"query": "What is happening in IRAN"})
# print(result)


# !pip install -qU langchain langchain-openai langchain-tavily
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:2b",
    temperature=0,
    # other params...
)

# Initialize the Tavily Search tool
tavily_search = TavilySearch(max_results=5, topic="general")

# Initialize the agent with the search tool
agent = create_agent(
    model=llm,
    tools=[tavily_search],
    system_prompt="You are a helpful research assistant. Use web search to find accurate, up-to-date information."
)

# Use the agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "What is the most popular sport in the world? Include only Wikipedia sources."}]
})

print(response)