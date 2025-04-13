from celery_app import app
from run_spider import run_spider

@app.task
def run_amazon_spider(item="pendrive", pages=1):
    run_spider('amazonspider',item,pages)