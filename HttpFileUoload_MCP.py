# HttpFileUpload_MCP.py
# This MCP is used to upload a local file to a huggingface space.
# The input is the absolute path to the local file and the full upload endpoint of the huggingface space.
# The output is the public URL of the uploaded file.

import os
import requests
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP("upload-mcp")

@mcp.tool
def upload_file(
    filepath: Annotated[str, "Absolute path to the local file to upload"],
    huggingface_space_url: Annotated[str, "Full upload endpoint of the huggingface space, e.g. 'https://jmiao24-alphagenome-mcp.hf.space'"]
) -> dict:
    """
    Upload a local file to the remote server.
    Input is the absolute path to the local file and the full upload endpoint. Output is the public URL of the uploaded file.
    """    
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "rb") as f:
        # key must match server expectation: "file"
        response = requests.post(huggingface_space_url + "/upload", files={"file": f})
    
    response.raise_for_status()
    result = response.json()
    return result[0] if isinstance(result, list) else result

if __name__ == "__main__":
    mcp.run()