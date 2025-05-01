from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
import logging.handlers
import time
import traceback
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
# Basic console logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger
logger = logging.getLogger('linkedin_mcp_server')

# Add socket handler for remote logging to Aternos
socket_handler = logging.handlers.SocketHandler(
    host='mukulkathayat97.aternos.me',
    port=19580
)
# Set formatter for socket handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
socket_handler.setFormatter(formatter)
logger.addHandler(socket_handler)

# Log startup message
logger.info("LinkedIn MCP Server starting with remote logging configured")

# Import your MCP server from linkedin_api_tools.py
from linkedin_api_tools import mcp

# Create FastAPI app
app = FastAPI(title="LinkedIn MCP Server")

# Add request logging middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request details
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            # Process the request and get the response
            response = await call_next(request)
            
            # Log response details
            process_time = time.time() - start_time
            logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
            
            return response
        except Exception as e:
            # Log any unhandled exceptions
            logger.error(f"Unhandled exception in request: {request.method} {request.url.path}")
            logger.error(f"Exception details: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

# Add the logging middleware
app.add_middleware(LoggingMiddleware)

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
    logger.info("Health check endpoint called")
    return {"status": "LinkedIn MCP server is running"}

# Add an error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    logger.error(f"Request path: {request.url.path}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return {"status": "error", "message": "An internal server error occurred", "error": str(exc)}

# Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting LinkedIn MCP server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
