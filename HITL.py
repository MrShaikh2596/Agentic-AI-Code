from langchain_ollama import ChatOllama
import time
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row  

load_dotenv()


llm = ChatOllama(
    #model="qwen3.5:0.8b",
    #model="qwen3.5:2b",
    model = "llama3.2:latest",
    temperature=0
)


res = llm.invoke("do you have tool-calling capabilities")

