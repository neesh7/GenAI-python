from fastapi import FastAPI, Query, Path  # basically creating an Rest API using FastAPI
from RAG_queues.worker_queue.connection import queue  # import the queue instance from connection.py
from RAG_queues.worker_queue.worker import process_query  # import the worker function to process the query
# from worker_queue.connection import queue  # import the queue instance from connection.py
# from worker_queue.worker import process_query  # import the worker function to process the query


# Building the FastAPI app
app = FastAPI()


# we have build 2 routes or endpoints
# 1. GET / - to check if the server is running
@app.get("/")
def root():
    return {"status": "Server is up and running"}

# 2. POST /chat - to process the query using RAG
@app.post("/chat")
def chat(
    query: str = Query(..., description="The query to process")
    ):
    # Here we will add the code to process the query using RAG and return the response
    # Basically this endpoint will take a query and return a response(your job recived )

    # query ko queue me daal dena hai
    # this below line is acting as producer who is putting the job in the queue
    job = queue.enqueue(process_query, query)  # process_query(query)  # enqueue the job to process the query
    # user ko bolo your job received
    return {"status": "Job enqueued", "job_id": job.id}

     
@app.get("/result/{job_id}")
def get_result(
    job_id: str = Path(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}