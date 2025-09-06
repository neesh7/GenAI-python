To use checkpointing we have to do these installs first
```bash
$ pip install -U pymongo langgraph langgraph-checkpoint-mongodb

$ uv add pymongo langgraph langgraph-checkpoint-mongodb
```

we are trying to implement checkpointer here
tableplus can help visualise the thread data

in chat_graph.py -- we are implementing checkpoint (persistence) using mongo db