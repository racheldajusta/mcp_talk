# MCP Talk

A simple MCP server with custom tools for interactive demos and automation. Includes tools for getting the current date and asking a Magic 8 Ball for fun, random answers.

## Features
- Get the current date in YYYY-MM-DD format
- Ask the Magic 8 Ball for a random response

## Installation
This project uses [uv](https://github.com/astral-sh/uv) and `pyproject.toml` for dependency management.

1. Clone this repository:
   ```sh
   git clone <your-repo-url>
   ```
2. Install [uv](https://github.com/astral-sh/uv) if you don't have it:
   ```sh
   pip install uv
   ```
3. Install dependencies:
   ```sh
   uv sync
   ```

## Usage
1. Start the MCP server:
   ```sh
   python main.py
   ```
2. Tools are available via the MCP API (see `mcp.json` for endpoint configuration).

### Example Tools
#### Get Current Date
Returns today's date in YYYY-MM-DD format.

#### Magic 8 Ball
Returns a random Magic 8 Ball answer to any yes/no question.

## API Endpoints
- `/tools/get_current_date` — Get the current date
- `/tools/magic_8_ball` — Get a Magic 8 Ball response

## License
MIT

## Contact
For questions or feedback, contact Rachel.
