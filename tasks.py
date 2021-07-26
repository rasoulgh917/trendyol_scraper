from celery import Celery
from search import main

app = Celery('tasks', broker='amqp://guest@80.208.230.14//')
app.control.rate_limit('myapp.mytask', '200/m')
@app.task
def main_caller(subcat_list, tablename):
    pass