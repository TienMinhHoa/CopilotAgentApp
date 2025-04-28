import json
from typing import cast
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import ToolMessage, AIMessage
from state import AgentState, Products

async def delete_node(state: AgentState, config: RunnableConfig):
    return state

async def perform_delete_node(state: AgentState, config: RunnableConfig):
    id = ""
    ai_message = cast(AIMessage, state["messages"][-2])
    tool_message = cast(ToolMessage, state["messages"][-1])

    if tool_message.content == 'YES':
        if ai_message.tool_calls:
            id = ai_message.tool_calls[0]["args"]["id"]
        else:
            parsed_tool_call = json.load(ai_message.additional_kwargs["function_call"]["arguments"])
            id = parsed_tool_call["id"]
    
    state["products"] = [i for i in state["products"] if i["id"] != id]
    return state