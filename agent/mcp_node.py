from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

async def main():
    model = ChatOpenAI(model="gpt-4o")
    async with MultiServerMCPClient(
        {
            "gmail": {
                "url": "https://mcp.composio.dev/composio/server/bbc037fb-be7a-4ec9-9ba4-322e83e2842a",
                "transport": "sse",
            }
        }
    ) as client:
        tools = client.get_tools()
        react_agent = create_react_agent(model, tools)
        print(tools)

        agent_input = {
            "messages": "Get latest news from hackernews"
        }
        agent_response = await react_agent.ainvoke(agent_input)
        print(agent_response)
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())