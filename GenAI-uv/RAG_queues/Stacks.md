## Tech Stacks used
- used Langchain libraries and openAI API and Embeddings
- QuadrantDB as a container using docker, check docker-compose.yml
- RQ used for setting up Messege Queues to prevent Rate Limitting
- Valkey used as Database to store intel from worker and provide update to user, we can use reddis too.
- Install FastAPI, uv add Fastapi
- we are using valkey in project as it is open source version of redis


## Steps
1. create docker-compose.yml to configure valkey as a container ( this is required for running messege queues which can be implemented using 'rq package' which uses reddis in the backend or so to say we will use valkey)
2. 
## Commands used
```bash
$ uv add Fastapi
# or do it using pip
$ pip install fastapi

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
$ python -m RAG_queues.main

# open independent terminal/server and run below command to run worker instance
$ rq worker --with-scheduler
```
# http://127.0.0.1:8000/docs#/default/chat_chat_post
<!-- rq is mainly built for docker payloads   -->
Error: if we don't run the app inside docker we will see this error called ``` AttributeError: module 'os' has no attribute 'fork'```
when we run the whole app inside docker then basically we mount our whole app inside docker itself

we are going to mount our whole vs code inside docker that's why we will be creating ```.devcontainer``` folder and inside that we will have `devcontainer.json`, `docker-compose.yml` and `dockerfile`

Install vscode extention 'Dev Container' then tap ctrl+shift+p and reload and open using extention. once you are inside sandboxed environment it means you dont have
the earlier dependency in you extention. use

```bash 
$ uv sync
$ uv venv
``` 
to bring back earlier dependency in any new pc or sandboxed enviornment

use $ source .venv/bin/activate -- to activate uv virtual environment

when running inside a contianer use the commands below
```bash
# make sure the terminal is in right env
$ source .venv/bin/activate
# to start the server or flask app
$ python -m RAG_queues.main
# to setup and start the messege queue for worker 
$ rq worker --with-scheduler --url redis://valkey:6379

$ rq worker --with-scheduler --url redis://valkey:6379

# run worker.sh which will provide openapikey as command line args
$ sh worker.sh

$ link 05-Rag1/.env RAG_queues/.env

# if you still face error while running it then pass it like this 

$ OPENAI_API_KEY=sk-xx python -m RAG_queues.main
```