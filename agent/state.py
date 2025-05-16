from typing import List, TypedDict
from langgraph.graph import MessagesState
from pydantic import Field


class Products(TypedDict):
    id:str
    name:str
    description:str
    cost:int
    
class Logs(TypedDict):
    message: str
    done: bool
    
class AgentState(MessagesState):
    agent_name: str
    model: str
    products: List[Products]
    log: List[Logs]
    images: List[dict] = Field(default_factory=list)  # For storing image data
    