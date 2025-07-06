uv init hello_agent
cd hello_agent
code .
uv venv
.venv\Scripts\activate
add uv dependencies-->  uv add openai-agents python-dotenv
create .env file
create .gitignore

uv run main.py