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
async def check_gmail_by_subject(subject: str) -> str:
    """Check Gmail for emails matching a subject and return snippets."""
    try:
        reader = GmailAPI()
        emails = reader.search_by_subject(subject)
        if not emails:
            return f"No emails found with subject: {subject}"
        return '\n'.join([f"ID: {email['id']}, Snippet: {email['snippet']}" for email in emails])
    except Exception as e:
        logger.error(f"Error checking Gmail: {e}")
        return f"Error: {e}"

@mcp.tool()
async def md_to_pdf(md_path: str, pdf_path: Optional[str] = None) -> str:
    """Converts a Markdown file to PDF with Bootstrap CSS styling. Optionally specify output path."""
    try:
        md_file = Path(md_path)
        if not md_file.exists():
            return f"Markdown file not found: {md_path}"
        html_content = markdown(md_file.read_text())
        bootstrap = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
        html_template = f"""
        <html>
        <head>{bootstrap}</head>
        <body class='container mt-4'>
            {html_content}
        </body>
        </html>
        """
        pdf_file = Path(pdf_path) if pdf_path else md_file.with_suffix('.pdf')
        HTML(string=html_template).write_pdf(str(pdf_file))
        return f"PDF created at: {pdf_file}"
    except Exception as e:
        logger.error(f"Error converting Markdown to PDF: {e}")
        return f"Error: {e}"

@mcp.tool()
async def send_email(to: str, subject: str, body: str, attachments: Optional[list] = None) -> str:
    """Send an email with optional attachments using the Gmail API."""
    try:
        reader = GmailAPI()
        result = reader.send_email(to, subject, body, attachments)
        return result
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return f"Error: {e}"