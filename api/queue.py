import os, redis, json

r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

def add_job(job):
    r.rpush("download_queue", json.dumps(job))

def get_job():
    job = r.blpop("download_queue", timeout=5)
    if job:
        return json.loads(job[1])
