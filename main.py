"""MCP Talk Server - A FastAPI application serving MCP tools."""

from fastapi import FastAPI, Request
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
import uvicorn
import logging

# Import MCP tools and configuration
from tools.tools import mcp
from config import server_config

# Configure logging
logging.basicConfig(level=getattr(logging, server_config.log_level.upper()))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MCP Talk Server",
    description="A server providing MCP tools for automation and demos",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

# Configure SSE transport
sse = SseServerTransport("/messages/")
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """Handle Server-Sent Events for MCP communication."""
    try:
        logger.info("Starting SSE connection")
        async with sse.connect_sse(request.scope, request.receive, request._send) as (
            read_stream,
            write_stream,
        ):
            init_options = mcp._mcp_server.create_initialization_options()
            
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                init_options,
            )
    except Exception as e:
        logger.error(f"Error in SSE handler: {e}")
        raise


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "MCP Talk Server is running"}


def main():
    """Main entry point for the application."""
    logger.info(f"Starting MCP Talk Server on {server_config.host}:{server_config.port}")
    uvicorn.run(
        app,
        host=server_config.host,
        port=server_config.port,
        log_level=server_config.log_level
    )


if __name__ == "__main__":
    main()