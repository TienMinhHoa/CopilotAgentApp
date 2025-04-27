import json
from typing import cast
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import ToolMessage, AIMessage
from state import AgentState, Products

async def add_node(state:AgentState, config: RunnableConfig):
    print(f"add node :{state}")
    return state

async def perform_add_product(state:AgentState, config: RunnableConfig):
    ai_message = cast(AIMessage, state["messages"][-2])
    tool_message = cast(ToolMessage, state["messages"][-1])
    print(f"ai message :{ai_message}")
    print(f"tool message: {tool_message}")
    if tool_message.content=="YES":
        if ai_message.tool_calls:
            id = ai_message.tool_calls[0]["args"]["id"]
            name= ai_message.tool_calls[0]["args"]["name"]
            description= ai_message.tool_calls[0]["args"]["description"]
            cost= int(ai_message.tool_calls[0]["args"]["cost"])
            
            product = Products(id,name,description,cost)
            
        else:
            parsed_tool_call = json.loads(ai_message.additional_kwargs["function_call"]["arguments"])
            id = parsed_tool_call["id"]
            name= parsed_tool_call["name"]
            description= parsed_tool_call["description"]
            cost= int(parsed_tool_call["cost"])
            product = Products(id,name,description,cost)
        state["products"].append(product)
    return state