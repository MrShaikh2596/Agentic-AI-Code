
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
load_dotenv()

# tool = TavilySearch(
#     max_results=5,
#     topic="general"
# )
# result = tool.invoke({"query": "What is happening in IRAN"})
# print(result)
# test = {"message": "Hello"}
# print(test.values().get)