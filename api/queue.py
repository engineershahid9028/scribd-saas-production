import os
import json
import redis

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_NAME = "job_queue"


def push_job(data: dict):
    r.rpush(QUEUE_NAME, json.dumps(data))


def pop_job(timeout=10):
    job = r.blpop(QUEUE_NAME, timeout=timeout)
    if job:
        return json.loads(job[1])
    return None
