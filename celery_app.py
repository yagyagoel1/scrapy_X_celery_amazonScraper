from celery import Celery 

app =  Celery('amazonscraper',
            broker="redis://localhost:6379/0",
            backend='redis://localhost:6379/0')

app.conf.task_routes={
    'tasks.run_amazon_spider':{'queue':'scrapy'}
}