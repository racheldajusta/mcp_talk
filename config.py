"""Configuration settings for MCP Talk Server."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    debug: bool = False
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv("MCP_HOST", cls.host),
            port=int(os.getenv("MCP_PORT", cls.port)),
            log_level=os.getenv("MCP_LOG_LEVEL", cls.log_level),
            debug=os.getenv("MCP_DEBUG", "false").lower() == "true"
        )


@dataclass
class ToolConfig:
    """Tool configuration settings."""
    mcp_server_name: str = "custom_mcp_tools"
    pdf_output_dir: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "ToolConfig":
        """Create configuration from environment variables."""
        return cls(
            mcp_server_name=os.getenv("MCP_SERVER_NAME", cls.mcp_server_name),
            pdf_output_dir=os.getenv("PDF_OUTPUT_DIR", cls.pdf_output_dir)
        )


# Global configuration instances
server_config = ServerConfig.from_env()
tool_config = ToolConfig.from_env()
