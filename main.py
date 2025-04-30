from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import your MCP server from linkedin_api_tools.py
from linkedin_api_tools import mcp

# Create FastAPI app
app = FastAPI(title="LinkedIn MCP Server")

# Add CORS middleware with full access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Mount the MCP server to the FastAPI app
app.mount("/mcp", mcp.app)

# Add a simple health check endpoint
@app.get("/")
async def root():
    return {"status": "LinkedIn MCP server is running"}

# Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
