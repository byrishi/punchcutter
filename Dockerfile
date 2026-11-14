# Punchcutter as a hosted MCP server (for ChatGPT and other remote clients).
#   docker build -t punchcutter . && docker run -p 8000:8000 -e PUNCHCUTTER_PUBLIC_URL=https://your.host punchcutter
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends libcairo2 libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir ".[mcp]"
ENV PUNCHCUTTER_WORKDIR=/data
EXPOSE 8000
CMD ["punchcutter", "mcp", "--http", "--host", "0.0.0.0", "--port", "8000"]
