import os, redis, json

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise RuntimeError("❌ REDIS_URL is not set in Railway")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def add_job(job):
    r.rpush("download_queue", json.dumps(job))

def get_job():
    job = r.blpop("download_queue", timeout=5)
    if job:
        return json.loads(job[1])
