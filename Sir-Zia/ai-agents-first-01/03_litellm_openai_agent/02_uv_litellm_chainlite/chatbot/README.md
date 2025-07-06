uv init chatbot
cd chatbot
code .
uv venv
.venv\Scripts\activate

add uv dependencies-->  uv add chainlit litellm python-dotenv 
create .env file
create .gitignore

Using uv to run the project

    uv run chainlit run main.py -w