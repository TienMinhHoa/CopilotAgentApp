from typing import List, cast, Literal, Annotated
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config
from langchain_openai import ChatOpenAI
from state import AgentState, Products
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

@tool
def add_products(
    id: Annotated[str,"The id of the product"],
    name: Annotated[str,"The name of the product"],
    description: Annotated[str,"The description of the product"],
    cost: Annotated[int,"The price of the product"]
):
    """
    Add the product to the table
    """
    
    
@tool
def delete_products(
    id: Annotated[str,"The id of the product"]
):
    """
    delete the product to the table
    """
    
@tool
def find_product():
    """find the products"""

@tool
def process_image(image_url:Annotated[str,"The url of the image"],
                  user_request: Annotated[str, "The user request"]):
    """Recieve an image url and process the request of user"""


llm = ChatOpenAI(model = "gpt-4o")

tools = [add_products,delete_products,process_image]
async def chat_node(state:AgentState, config: RunnableConfig) :
    print("humman messages: ",state)
    state["products"] = state.get("products", [])
    
    llm_with_tools = llm.bind_tools(
        [
            *tools
        ],
        parallel_tool_calls=False,
    )

    system_message = """
        You are an agent that helps users manage inventory information, including phone products. 
        You help users add, delete, and search for products. 
        You also help users process images and return all the component in the image. 
        Becarefull when processing image, the image_path is a url.
    """
   
    response = await llm_with_tools.ainvoke(
        [
            SystemMessage(content = system_message),
            *state["messages"]
        ],
        config = config
    )
    ai_message = cast(AIMessage,response)
    # if ai_message.tool_calls:
    #     if ai_message.tool_calls[0]["name"] == "add_products":
    #         state["messages"] =  [ai_message,ToolMessage(
    #                     tool_call_id=ai_message.tool_calls[0]["id"],
    #                     content="Research question written.")]
    #         print(f"#####################{state}######################")
    #         return state
    
    state["messages"] = [ai_message]
    print(f"################# state of agent{state} ###############")
    return {
        "messages": [response],
        "products": state.get("products", [])
    }
        