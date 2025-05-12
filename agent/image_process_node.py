import json
from typing import cast
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from state import AgentState, Products
import base64
import httpx
import os
from dotenv import load_dotenv
from openai import OpenAI
import fitz
from PIL import Image
import io

from langchain_openai import ChatOpenAI


load_dotenv()


async def encode_pdf_from_url(pdf_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(pdf_url)
            response.raise_for_status()
            pdf_data = response.content
            pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error loading image: {e}\n")
        return None
    

async def encode_image_from_url(url:str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            image_data = response.content
            return base64.b64encode(image_data).decode("utf-8")
    except Exception as e:
        print(f"Error loading image: {e}\n")
        return None

async def process_file_node(state:AgentState, config: RunnableConfig):
    llm = ChatOpenAI(model="gpt-4o-mini")
    url_file = state["messages"][-1].tool_calls[0]["args"]["url"]
    user_request = state["messages"][-1].tool_calls[0]["args"]["user_request"]
    # print(url_file)

    if ".jpg" in url_file:
        base64_image = await encode_image_from_url(url_file)
    elif "pdf" in url_file:
        base64_image = await encode_pdf_from_url(url_file)

    message = HumanMessage(
    content=[
        {"type": "text", "text": user_request},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        },
        ],
    )


    response = await llm.ainvoke([message])

    tool_message = ToolMessage(
        content= response.content,
        tool_call_id=state["messages"][-1].tool_calls[0]["id"]
    )
    state["messages"].append(tool_message)
    return state


if __name__ == "__main__":
    import asyncio
    # url = "https://7715496.fs1.hubspotusercontent-na1.net/hub/7715496/hubfs/B%E1%BA%A3n%20v%E1%BA%BD%20thi%E1%BA%BFt%20k%E1%BA%BF%20n%E1%BB%99i%20th%E1%BA%A5t%20nh%C3%A0%20ph%E1%BB%91/ho-so-thiet-ke-nha-pho%20(2).jpg?quality=low&width=1000&height=666&name=ho-so-thiet-ke-nha-pho%20(2).jpg"
    # a = asyncio.run(process_image_node(AgentState(messages=[url]), config=RunnableConfig()))
    # print(a["messages"][-1])


    

    
    
