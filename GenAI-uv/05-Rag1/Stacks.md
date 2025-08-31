## Tech Stacks used
- used Langchain libraries and openAI API and Embeddings
- QuadrantDB as a container using docker, check docker-compose.yml
- RQ used for setting up Messege Queues to prevent Rate Limitting
- Valkey used as Database to store intel from worker and provide update to user, we can use reddis too.


```bash 
$ pip install -qU langchain_community pypdf

# to perform chunking
$ pip install -qU langchain-text-splitters

# to do vector embeddings langchain provides it's own wrapper and to use it install below module
$ pip install langchain-openai
```

#### Setting up QuadrantDB for our projects
1. create a docker-compose.yml
2. $ docker compose -f <docker-compose.yml> up -d 
3. $ docker compose down
4. Use langchain wrapper of quadrant vector store