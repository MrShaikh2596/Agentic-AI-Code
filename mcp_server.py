import os
import requests
from dotenv import load_dotenv
from fastmcp.server.server import FastMCP
from fastmcp.tools import tool
from langchain_tavily import TavilySearch

load_dotenv()

search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

@tool(
    name="tavily_search",
    description="Search current web content and return structured results.",
)
def tavily_search(query: str) -> dict:
    """
    Perform a Tavily search for the given query.
    """
    return search_tool.invoke({"query": query})

@tool(
    name="calculator",
    description="Perform basic arithmetic operations: add, sub, mul, div.",
)
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}

        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result,
        }
    except Exception as e:
        return {"error": str(e)}

@tool(
    name="get_stock_price",
    description="Fetch latest stock price for a symbol using Alpha Vantage.",
)
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA').
    """
    api_key = os.getenv("ALPHAVANTAGE_API_KEY", "YVY4J6UVY3H32AP8")
    url = (
        f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}"
        f"&apikey={api_key}"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

mcp_server = FastMCP(
    name="AgenticAI Tools Server",
    instructions="A backend MCP server exposing Tavily search, calculator, and stock price tools.",
    version="1.0",
)

mcp_server.add_tool(tavily_search)
mcp_server.add_tool(calculator)
mcp_server.add_tool(get_stock_price)

if __name__ == "__main__":
    mcp_server.run(transport="http", host="0.0.0.0", port=8200)
