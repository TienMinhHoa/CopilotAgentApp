from typing import List, TypedDict
from langgraph.graph import MessagesState


class Products(TypedDict):
    id:str
    name:str
    description:str
    cost:int
    
class Logs(TypedDict):
    message: str
    done: bool
    
class AgentState(MessagesState):
    model: str
    products: List[Products]
    log: List[Logs]
    