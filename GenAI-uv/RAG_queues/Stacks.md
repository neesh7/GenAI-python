## Tech Stacks used
- used Langchain libraries and openAI API and Embeddings
- QuadrantDB as a container using docker, check docker-compose.yml
- RQ used for setting up Messege Queues to prevent Rate Limitting
- Valkey used as Database to store intel from worker and provide update to user, we can use reddis too.
- Install FastAPI, uv add Fastapi


## Commands used
```bash
$ uv add Fastapi

$ fastapi dev server.py # if using pi

# if using uv then
$ uv pip install "fastapi[standard]"
$ uv run fastapi dev server.py

# Add RQ as our messege queue will be in rq db
$ pip install rq
$ uv add rq

$ uv add uvicorn

$ python -m rag_queue.main

$ python -m 06-RAG-queues.main

# open independent terminal/server and run below command to run worker instance
$ rq worker --with-scheduler
```
# http://127.0.0.1:8000/docs#/default/chat_chat_post