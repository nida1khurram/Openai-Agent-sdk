Initiolize chainlit project in 04_hello_agent -->sync folder
1. uv init --package hello_agent
2. cd hello_agent
3. code .
4. uv venv
5. .venv\Scripts\activate
6. add uv dependencies-->  uv add chainlit google-generativeai python-dotenv
7. create --> .env file 
8. create --> main.py file
9. create --> .gitignore
10. cd src--> cd hello_agent
11. uv run chainlit run main.py -w
