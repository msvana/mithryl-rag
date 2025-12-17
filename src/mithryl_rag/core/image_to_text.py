import base64
import subprocess
import tempfile
from pathlib import Path

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama

from mithryl_rag.config import VISION_LLM, OLLAMA_BASE_URL


PROMPT = """
You are a helpful assistant that can turn images into text.

Your task is to create the most accurate text description of
the provided image. 

If the image contains a diagram, try to replicate it using
the mermaid syntax. If the image contains a table, try to
replicate it using the markdown syntax.

Otherwise, just describe the image in as much detail as possible.
"""


class ImageToText:
    def __init__(self, llm: str = VISION_LLM, ollama_base_url: str = OLLAMA_BASE_URL):
        self._llm = ChatOllama(
            model=llm, temperature=0.0, max_tokens=512, base_url=ollama_base_url
        )
        self._agent = create_agent(self._llm, system_prompt=PROMPT)

    def analyze_image(self, image_contents: str) -> str:
        metadata, data = image_contents.split(";base64,")
        mimetype = metadata.replace("data:image/", "")

        if mimetype == "x-emf":
            data = emf_to_png_base64(data)
            mimetype = "image/png"

        response = self._agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content_blocks=[
                            {"type": "image", "base64": data, "mime_type": mimetype}
                        ]
                    )
                ]
            }
        )

        return response["messages"][-1].content


def emf_to_png_base64(base64_emf: str, dpi: int = 96) -> str:
    emf_data = base64.b64decode(base64_emf)

    with tempfile.NamedTemporaryFile(suffix=".emf", delete=False) as temp_emf:
        temp_emf.write(emf_data)
        temp_emf_path = temp_emf.name

    temp_png_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    output_path = temp_png_file.name
    temp_png_file.close()
    temp_png = True

    cmd = ["inkscape", "--export-dpi", str(dpi), "-o", output_path, temp_emf_path]
    subprocess.run(cmd, capture_output=True, text=True, check=True)

    with open(output_path, "rb") as f:
        png_data = f.read()
        png_base64 = base64.b64encode(png_data).decode("utf-8")

    if temp_png:
        Path(output_path).unlink()

    return png_base64
