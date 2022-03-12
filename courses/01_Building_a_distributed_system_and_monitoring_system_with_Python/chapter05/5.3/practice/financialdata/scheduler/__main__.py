import datetime
import time
from functools import partial

from apscheduler.schedulers.background import BackgroundScheduler
from financialdata.producer import update
from financialdata.scheduler.crawler_data import save_dataset_count_daily
from loguru import logger


def main():
    today = (
        datetime.datetime.utcnow() +
        datetime.timedelta(hours=8)
        ).strftime("%Y-%m-%d")
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="taiwan_stock_price",
        func=partial(
            update,
            dataset="taiwan_stock_price",
            start_date=today,
            end_date=today,
        ),
        trigger="cron",
        hour="15",
        minute="0",
        day_of_week="mon-fri",
        second="0",
    )
    scheduler.add_job(
        save_dataset_count_daily,
        "cron",
        day_of_week="mon-sat",
        hour="*",
        minute="*/1",
    )
    logger.info("add scheduler")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(10)
