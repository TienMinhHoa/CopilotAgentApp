import json
from typing import cast
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import ToolMessage, AIMessage
from state import AgentState, Products
from langgraph.types import interrupt 

async def add_node(state:AgentState, config: RunnableConfig):
    print(f"add node")
    # state["messages"].append(ToolMessage(content="YES",tool_call_id = state["messages"][-1].tool_calls[0]["id"]))
    print(state["messages"][-1])
    print("tools",state["messages"][-1].tool_calls[0]["args"])
    content = interrupt(state["messages"][-1].tool_calls[0]["args"])

    state["messages"].append(ToolMessage(content=content,tool_call_id = state["messages"][-1].tool_calls[0]["id"]))
    return state

async def perform_add_product(state:AgentState, config: RunnableConfig):
    ai_message = cast(AIMessage, state["messages"][-2])
    tool_message = cast(ToolMessage, state["messages"][-1])
    print(f"ai message :{ai_message.content}")
    print(f"tool message: {tool_message.content}")
    if tool_message.content=="YES":
        # print
        if ai_message.tool_calls:
            id = ai_message.tool_calls[0]["args"]["id"]
            name= ai_message.tool_calls[0]["args"]["name"]
            description= ai_message.tool_calls[0]["args"]["description"]
            cost= int(ai_message.tool_calls[0]["args"]["cost"])
            
            product = {
                    "id": id,
                    "name": name,
                    "description": description,
                    "cost": cost
                }
            
        else:
            parsed_tool_call = json.loads(ai_message.additional_kwargs["function_call"]["arguments"])
            id = parsed_tool_call["id"]
            name= parsed_tool_call["name"]
            description= parsed_tool_call["description"]
            cost= int(parsed_tool_call["cost"])
            product = {
                    "id": id,
                    "name": name,
                    "description": description,
                    "cost": cost
                }
        # print(product)
        state["products"].append(product)
        # print(state["products"])
    return state