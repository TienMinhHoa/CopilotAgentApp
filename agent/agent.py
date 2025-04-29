import json
from typing import cast

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from chat import chat_node
from add import add_node, perform_add_product
from delete import delete_node, perform_delete_node
def route(state: AgentState):
    """Route after the chat node."""
    messages = state.get("messages", [])
    if messages and isinstance(messages[-1], AIMessage):
        ai_message = cast(AIMessage, messages[-1])
        
        # If the last AI message has tool calls we need to determine to route to the
        # trips_node or search_node based on the tool name.
        if ai_message.tool_calls:
            tool_name = ai_message.tool_calls[0]["name"]
            if tool_name in ["add_products", "delete_products"]:
                if tool_name == "add_products":
                    return "add_product"
                if tool_name == "delete_products":
                    return "delete_product"
    if messages and isinstance(messages[-1], ToolMessage):
        return "chat_node"
    
    return END

workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("add_product",add_node)
workflow.add_node("perform_add_product", perform_add_product)
workflow.add_node("delete_product",delete_node)
workflow.add_node("perform_delete_node", perform_delete_node)

memory = MemorySaver()
# workflow.set_entry_point(START)
workflow.add_conditional_edges("chat_node", route, ["add_product", "chat_node", "delete_product", END])

workflow.add_edge(START,"chat_node")
workflow.add_edge("add_product","perform_add_product")
workflow.add_edge("perform_add_product", "chat_node")
workflow.add_edge("perform_delete_node","chat_node")
workflow.add_edge("delete_product", "perform_delete_node")


graph = workflow.compile( checkpointer=memory,interrupt_after=["add_product","delete_product"])