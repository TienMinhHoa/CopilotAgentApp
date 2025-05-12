import os
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint 
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent 
from fastapi.middleware.cors import CORSMiddleware
from agent import graph 
 
from dotenv import load_dotenv
load_dotenv()
 
app = FastAPI()

origins = [
    "*",  # IP của máy frontend
    # Hoặc dùng "*" nếu muốn cho phép tất cả (chỉ dùng khi bạn biết chắc an toàn)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # hoặc ["*"] để cho phép tất cả
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="manager", # the name of your agent defined in langgraph.json
            description="tesst agent",
            graph=graph, # the graph object from your langgraph import
        )
    ],
)
 
# Use CopilotKit's FastAPI integration to add a new endpoint for your LangGraph agents
add_fastapi_endpoint(app, sdk, "/copilotkit")
 
# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}
 
def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "server:app", 
        host="0.0.0.0",
        port=port,
        reload=True,
    )