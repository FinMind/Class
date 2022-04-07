import datetime
import time
from functools import partial

from apscheduler.schedulers.background import BackgroundScheduler
from financialdata.producer import update
from loguru import logger


def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="taiwan_stock_price",
        func=partial(
            update,
            dataset="taiwan_stock_price",
        ),
        trigger="cron",
        hour="15",
        minute="0",
        day_of_week="mon-fri",
        second="0",
    )
    logger.info("add scheduler")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)
