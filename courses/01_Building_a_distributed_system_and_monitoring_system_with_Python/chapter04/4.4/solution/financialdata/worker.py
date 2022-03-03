import importlib
import socket
import time
import typing

import pymysql
from loguru import logger

from celery import Celery, Task
from financialdata import db
from financialdata.config import (
    MESSAGE_QUEUE_HOST,
    MESSAGE_QUEUE_PORT,
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
)


class CallbackTask(Task):
    def retry(
        self, kwargs: typing.List[typing.Union[str, typing.Dict[str, str]]]
    ):
        """如果任務失敗，重新發送"""
        logger.info(f"retry: {kwargs}")
        crawler = getattr(
            importlib.import_module("financialdata.tasks"), "crawler"
        )
        dataset = kwargs.get("dataset")
        parameters = kwargs.get("parameters")
        task = crawler.s(dataset=dataset, parameters=parameters)
        task.apply_async(queue=parameters.get("data_source", ""))

    def on_success(self, retval, task_id, args, kwargs):
        return super(CallbackTask, self).on_success(
            retval, task_id, args, kwargs
        )

    def on_failure(self, exc, task_id, args, kwargs, info):
        """如果任務失敗，重新發送"""
        sql = """INSERT INTO `celery_log`(
                `retry`,`status`,`worker`, `task_id`, `msg`, `info`, `args`, `kwargs`)
                 VALUES ('0','-1', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(
            socket.gethostname(),
            task_id,
            pymysql.converters.escape_string(str(exc)),
            pymysql.converters.escape_string(str(info)),
            pymysql.converters.escape_string(str(args)),
            pymysql.converters.escape_string(str(kwargs)),
        )
        db.commit(sql=sql, mysql_conn=db.router.mysql_financialdata_conn)
        logger.info(f"args: {args}")
        logger.info(f"kwargs: {kwargs}")
        self.retry(kwargs)
        time.sleep(3)
        return super(CallbackTask, self).on_failure(
            exc, task_id, args, kwargs, info
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
