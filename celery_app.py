from celery import Celery 

app =  Celery('amazonscraper',
            broker="redis://redis:6379/0",
            backend='redis://redis:6379/0')

app.conf.task_routes={
    'tasks.run_amazon_spider':{'queue':'scrapy'}
}