from langchain_ollama import ChatOllama
import time
from dotenv import load_dotenv
load_dotenv()


llm = ChatOllama(
    #model="qwen3.5:0.8b",
    #model="qwen3.5:2b",
    model = "llama3.2:latest",
    temperature=0
)

t1 = time.time()
res = llm.invoke("do you have tool-calling capabilities")
t2=time.time()
print(res.content,"time:taken:",t2-t1)