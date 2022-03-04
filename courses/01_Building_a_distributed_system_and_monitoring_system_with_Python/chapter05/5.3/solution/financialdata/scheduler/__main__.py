import time
from loguru import logger

from apscheduler.schedulers.background import BackgroundScheduler
from financialdata.scheduler.crawler_data import save_dataset_count_daily


def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        save_dataset_count_daily,
        "cron",
        day_of_week="mon-sat",
        hour="*",
        minute="*/1",
    )
    scheduler.start()
    logger.info("scheduler start")


if __name__ == "__main__":
    main()
    while True:
        time.sleep(10)
