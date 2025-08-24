from fastapi import FastAPI, Query # basically creating an Rest API using FastAPI
from RAG_queues.worker_queue.connection import queue  # import the queue instance from connection.py
from RAG_queues.worker_queue.worker import process_query  # import the worker function to process the query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Server is up and running"}

@app.post("/chat")
def chat(
    query: str = Query(..., description="The query to process")
    ):
    # Here we will add the code to process the query using RAG and return the response
    # Basically this endpoint will take a query and return a response(your job recived )

    # query ko queue me daal dena hai
    job = queue.enqueue(process_query, query)  # process_query(query)  # enqueue the job to process the query
    # user ko bolo your job received
    return {"status": "Job enqueued", "job_id": job.id}
    