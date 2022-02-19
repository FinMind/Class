from celery import Celery
from financialdata.config import (
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
    MESSAGE_QUEUE_HOST,
    MESSAGE_QUEUE_PORT,
)

broker = (
    f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@"
    f"{MESSAGE_QUEUE_HOST}:{MESSAGE_QUEUE_PORT}/"
)
app = Celery(
    "task",
    # 只包含 tasks.py 裡面的程式, 才會成功執行
    include=["financialdata.tasks"],
    # 連線到 rabbitmq,
    # pyamqp://user:password@localhost:5672/
    # 本書的帳號密碼都是 worker
    broker=broker,
)
