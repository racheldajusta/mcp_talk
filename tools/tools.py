from fastmcp import FastMCP
from datetime import datetime
import random
from markdown import markdown
from weasyprint import HTML
import os
from pathlib import Path
from typing import Optional
import logging

# Import configuration
from config import tool_config
from .gmail_reader import GmailReader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(tool_config.mcp_server_name)


# Constants
MAGIC_8_BALL_RESPONSES = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes – definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
]


@mcp.tool()
async def magic_8_ball() -> str:
    """Get a random Magic 8 Ball response."""
    try:
        return random.choice(MAGIC_8_BALL_RESPONSES)
    except Exception as e:
        logger.error(f"Error generating Magic 8 Ball response: {e}")
        return f"Error: {e}"


@mcp.tool()
async def md_to_pdf(md_path: str, pdf_path: Optional[str] = None) -> str:
    """Convert a Markdown file to PDF with Bootstrap styling.
    
    Args:
        md_path: Path to the Markdown file
        pdf_path: Optional output path. If not provided, uses md_path with .pdf extension
        
    Returns:
        Success message with PDF path or error message
    """
    try:
        md_file = Path(md_path)
        if not md_file.exists():
            return f"Error: Markdown file not found: {md_path}"
        
        # Read markdown content
        md_content = md_file.read_text(encoding='utf-8')
        html_content = markdown(md_content)
        
        # Apply Bootstrap styling
        bootstrap_link = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
        html_full = f"<html><head>{bootstrap_link}</head><body class='container mt-4'>{html_content}</body></html>"
        
        # Determine output path
        if pdf_path is None:
            pdf_path = str(md_file.with_suffix('.pdf'))
        
        # Generate PDF
        HTML(string=html_full).write_pdf(pdf_path)
        logger.info(f"PDF successfully created at: {pdf_path}")
        return f"PDF created at: {pdf_path}"
        
    except FileNotFoundError as e:
        error_msg = f"File not found: {e}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Error converting markdown to PDF: {e}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


@mcp.tool()
async def check_gmail_by_subject(subject: str) -> str:
    """Check Gmail for emails matching a subject and return snippets."""
    try:
        reader = GmailReader()
        emails = reader.search_by_subject(subject)
        if not emails:
            return f"No emails found with subject: {subject}"
        return '\n'.join([f"ID: {email['id']}, Snippet: {email['snippet']}" for email in emails])
    except Exception as e:
        logger.error(f"Error checking Gmail: {e}")
        return f"Error: {e}"