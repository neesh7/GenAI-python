```bash
$ pip install mem0ai
# spin up qdb first
$ docker compose up

$ pip install langchain_neo4j
```
# http://localhost:7474/browser/
# http://localhost:6333/dashboard#/welcome

Adding to memory part happens in Async Queue

Neo4j uses cipher queries
MATCH (a)-[r]->(b) RETURN a, r, b