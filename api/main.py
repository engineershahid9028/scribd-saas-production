from fastapi import FastAPI, Request
from api.queue import add_job
import uuid

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "App is running"}

@app.post("/job")
async def create_job(req: Request):
    data = await req.json()

    job_id = str(uuid.uuid4())

    job = {
        "job_id": job_id,
        "user_id": data["user_id"],
        "msg_id": data["msg_id"],
        "url": data["url"]
    }

    add_job(job)

    return {"status": "queued", "job_id": job_id}
