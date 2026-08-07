import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

# Load variables from a .env file into os.environ
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_TEAM_ID = os.getenv("SLACK_TEAM_ID")

if not SLACK_BOT_TOKEN or not SLACK_TEAM_ID:
    raise RuntimeError(
        "Set SLACK_BOT_TOKEN and SLACK_TEAM_ID in your environment or .env file before running this script."
    )

client = MultiServerMCPClient(
    {
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




async def test_slack_list_channels():
    async with client.session("slack") as session:
        tools = await load_mcp_tools(session)
        slack_list_channels = tools[0]
        print(await slack_list_channels.ainvoke({}))


async def test_slack_post_message():
    async with client.session("slack") as session:
        tools = await load_mcp_tools(session)
        slack_post_message = tools[1]
        print(await slack_post_message.ainvoke({"channel_id": "C0BH29TPC3F", "text": "Hello from MCP client!"}))




if __name__ == "__main__":
    asyncio.run(test_slack_post_message())