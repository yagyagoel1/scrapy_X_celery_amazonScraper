from fastapi import FastAPI
from tasks import run_amazon_spider


app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"success":1}

@app.get("/")
def startScraping():
    run_amazon_spider.delay()
    return {"success":1,"message":"scraping started"}





