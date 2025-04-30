FROM python:3.12.3

WORKDIR /app

COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

COPY . .

# Use MCP CLI with stdio transport instead of uvicorn
CMD ["mcp", "serve", "linkedin_api_tools:mcp"]