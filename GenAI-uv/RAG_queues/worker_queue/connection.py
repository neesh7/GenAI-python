from redis import Redis
from rq import Queue


queue = Queue(connection=Redis()) # create a queue instance