# MCP Talk

Repo for Rachel Da Justa's talk on MCP.

## Features
- Get the current date in YYYY-MM-DD format
- Ask the Magic 8 Ball for a random response

## Installation
This project uses [uv](https://github.com/astral-sh/uv) and `pyproject.toml` for dependency management. Python 3.11+ is recommended.


1. (Optional but recommended) Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install [uv](https://github.com/astral-sh/uv) if you don't have it:
   ```sh
   pip install uv
   ```
3. Install dependencies:
   ```sh
   uv sync
   ```

If you encounter issues, ensure you are using a compatible Python version and that `uv` is installed in your active environment.

## Usage
1. Start the MCP server:
   ```sh
   python main.py
   ```
2. Tools are available via the MCP API (see `mcp.json` for endpoint configuration).

## MCP Integration in VS Code

To add this server to your MCP configuration in Visual Studio Code:

1. Open `.vscode/mcp.json` in your project folder.
2. Add or update the `servers` section to include your MCP server:
   ```jsonc
   {
     "servers": {
       "my_tools": {
         "url": "http://localhost:8000/sse"
       }
       // ...other servers...
     }
   }
   ```
3. Save the file. Your MCP server will now be available for use in VS Code MCP workflows.

For more details, see the [MCP documentation](https://github.com/anthropic/model-context-protocol).

## License
MIT

## Contact
For questions or feedback, contact Rachel.
