from fastapi import FastAPI,HTTPException
from tasks import run_amazon_spider
from dotenv import load_dotenv
import os
from .types import dataBody
load_dotenv()

app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"success":1}

@app.get("/{key}")
def startScraping(key):
    if key != os.getenv('KEY_TO_SCRAPE'):
        raise HTTPException(401,"Unauthorized")
    run_amazon_spider.delay()
    return {"success":1,"message":"scraping started"}




@app.post("/{key}")
def startScraping(key,payload:dataBody):
    if key != os.getenv('KEY_TO_SCRAPE'):
        raise HTTPException(401,"Unauthorized")
    
    task= run_amazon_spider.delay(item = payload.item,pages=payload.noOfPages)
    print(task)
    return {"success":1,"message":"scraping started","taskId":str(task)}

@app.get("/task/{task_id}")
def get_task_status(task_id: str):
    task = run_amazon_spider.AsyncResult(task_id)
    if task.state == 'PENDING':
        return {"status": "pending"}
    elif task.state == 'SUCCESS':
        return {"status": "completed"}
    else:
        return {"status": "failed", "error": str(task.info)}