from fastmcp import FastMCP
from datetime import datetime
import random
from markdown import markdown
from weasyprint import HTML
import os

mcp = FastMCP("custom_mcp_tools ")


@mcp.tool()
async def get_current_date() -> str:
    """Get current date
    """
    return str(datetime.today().strftime('%Y-%m-%d'))


@mcp.tool()
async def magic_8_ball() -> str:
    """Get a random Magic 8 Ball response"""
    responses = [
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
    return random.choice(responses)


@mcp.tool()
async def md_to_pdf(md_path: str, pdf_path: str = None) -> str:
    """Convert a Markdown file to PDF. Args:
    md_path: Path to the Markdown file.
    pdf_path: Optional path to save the PDF. If not provided, saves as md_path.pdf
    Returns: Path to the generated PDF file.
    """
    if not os.path.isfile(md_path):
        return f"Markdown file not found: {md_path}"
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html_content = markdown(md_content)
    # Use Bootstrap CSS for improved PDF appearance
    bootstrap_link = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
    html_full = f"<html><head>{bootstrap_link}</head><body class='container mt-4'>{html_content}</body></html>"
    if not pdf_path:
        pdf_path = md_path.rsplit('.', 1)[0] + '.pdf'
    HTML(string=html_full).write_pdf(pdf_path)
    return f"PDF created at: {pdf_path}"