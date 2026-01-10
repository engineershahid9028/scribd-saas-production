import os, redis, json

r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
QUEUE = "download_queue"

def add_job(job):
    r.rpush(QUEUE, json.dumps(job))

def get_job():
    job = r.blpop(QUEUE, timeout=5)
    if job:
        return json.loads(job[1])

