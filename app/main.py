from fastapi import FastAPI,HTTPException
from tasks import run_amazon_spider
from dotenv import load_dotenv
import os
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





