from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()
import requests
search_tool = TavilySearch(
    max_results=5,
    topic="general"
)

@tool("calculator")
async def calculator(first_num: float, second_num: float, operation: str) -> dict:
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
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool("get_stock_price")
async def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=YVY4J6UVY3H32AP8"
    r =  requests.get(url)
    return r.json()
# tools = [get_stock_price, calculator,search_tool]

# from langchain_core.utils.function_calling import convert_to_openai_tool
# for t in tools:
#     print(type(t), getattr(t, "name", None), getattr(t, "description", None))
#     print(convert_to_openai_tool(t))