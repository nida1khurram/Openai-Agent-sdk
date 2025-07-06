create folder multi-agent-system 
in multi-agent-system
uv init .
uv venv
.venv\Scripts\activate
uv run main.py
uv add chainlit openai-agents dotenv

uv --help