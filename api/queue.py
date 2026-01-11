import os
import redis
import json

REDIS_URL = os.getenv("REDIS_URL")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_NAME = "download_queue"

def add_job(job):
    r.rpush(QUEUE_NAME, json.dumps(job))

def get_job():
    job = r.blpop(QUEUE_NAME, timeout=5)
    if job:
        return json.loads(job[1])
    return None
