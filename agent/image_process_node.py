import json
from typing import cast
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import ToolMessage, AIMessage
from state import AgentState, Products
import base64
from google import genai
from google.genai import types
import httpx
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))



async def encode_image(url:str):
    print(url)
    try:
        async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                image_bytes = response.content
                image = await types.Part.from_bytes(
                    data=image_bytes, mime_type="image/jpeg"
                )
                return image
    except Exception as e:
        print(f"Error loading image: {e}\n")
        return None


async def process_image_node(state:AgentState, config: RunnableConfig):
    print(f"process image node :{state}")
    image_path = state["messages"][-1].tool_calls[0]["args"]["image_url"]
    user_request = state["messages"][-1].tool_calls[0]["args"]["user_re quest"]
    print(image_path)


    client = OpenAI()
    try:
        response = client.responses.create(
            model="gpt-4o",
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_request},
                    {
                        "type": "input_image",
                        "image_url":image_path,
                    },
                ],
            }],
        )
    except Exception as e:
        print(f"Error: {e}")
        return state
    print(f"response: {response}")
    ai_response = ToolMessage(
        content=response.output_text,
        tool_call_id=state["messages"][-1].tool_calls[0]["id"]
    )
    state["messages"].append(ai_response)

    return state


if __name__ == "__main__":
    import asyncio
    url = "https://7715496.fs1.hubspotusercontent-na1.net/hub/7715496/hubfs/B%E1%BA%A3n%20v%E1%BA%BD%20thi%E1%BA%BFt%20k%E1%BA%BF%20n%E1%BB%99i%20th%E1%BA%A5t%20nh%C3%A0%20ph%E1%BB%91/ho-so-thiet-ke-nha-pho%20(2).jpg?quality=low&width=1000&height=666&name=ho-so-thiet-ke-nha-pho%20(2).jpg"
    a = asyncio.run(process_image_node(AgentState(messages=[url]), config=RunnableConfig()))
    print(a["messages"][-1])


    

    
    
