import base64
import io
import requests
import fitz
from PIL import Image
from state import AgentState
from langchain_core.runnables import RunnableConfig
def pdf_page_to_base64(pdf_url: str, page_number: int):
    # Tải PDF từ URL
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_data = response.content
    
    # Mở PDF từ dữ liệu đã tải
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    page = pdf_document.load_page(page_number - 1)  # input is one-indexed
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def pdf_process_node(state:AgentState, config: RunnableConfig):
    print(f"process image node :{state}")
    image_path = state["messages"][-1].tool_calls[0]["args"]["pdf_url"]
    user_request = state["messages"][-1].tool_calls[0]["args"]["user_request"]
    print(image_path)
    
    base64_image = pdf_page_to_base64(image_path, 1)
    
    # Thêm tool message response
    tool_message = ToolMessage(
        content="PDF processed successfully",
        tool_call_id=state["messages"][-1].tool_calls[0]["id"]
    )
    state["messages"].append(tool_message)
    
    return state
    
    