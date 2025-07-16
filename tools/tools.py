from fastmcp import FastMCP
from pathlib import Path
from markdown import markdown
from weasyprint import HTML
from typing import Optional
import logging

# Import configuration
from config import tool_config
from .gmail_reader import GmailAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(tool_config.mcp_server_name)

@mcp.tool()
async def search_gmail_by_subject(subject: str) -> str:
    """Search Gmail for emails matching a subject and return snippets."""
    try:
        reader = GmailAPI()
        emails = reader.search_by_subject(subject)
        if not emails:
            return f"No emails found with subject: {subject}"
        return '\n'.join([f"ID: {email['id']}, Snippet: {email['snippet']}" for email in emails])
    except Exception as e:
        logger.error(f"Error searching Gmail: {e}")
        return f"Error: {e}"

@mcp.tool()
async def md_to_pdf(md_path: str, pdf_path: Optional[str] = None) -> str:
    """Convert a Markdown file to PDF using Bootstrap CSS for styling."""
    try:
        md_file = Path(md_path)
        if not md_file.exists():
            return f"Markdown file not found: {md_path}"
        html_content = markdown(md_file.read_text(encoding='utf-8'))
        # Use Bootstrap CSS from CDN
        bootstrap_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
        html = f"""
        <html>
        <head>
        <meta charset='utf-8'>
        <title>Document</title>
        {bootstrap_css}
        </head>
        <body><div class='container my-5'>{html_content}</div></body>
        </html>
        """
        if not pdf_path:
            pdf_path = str(md_file.with_suffix('.pdf'))
        HTML(string=html).write_pdf(pdf_path)
        return f"PDF generated at: {pdf_path}"
    except Exception as e:
        logger.error(f"Error converting Markdown to PDF: {e}")
        return f"Error: {e}"



