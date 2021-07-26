from celery import Celery
from search import main

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def main_caller(subcat_list, tablename):
    return main(subcat_list, tablename)