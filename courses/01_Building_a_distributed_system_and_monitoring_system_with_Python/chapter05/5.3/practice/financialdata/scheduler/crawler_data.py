import datetime
import typing
import pandas as pd

from loguru import logger

from financialdata.db import router, query
from financialdata.db.db import upload_data, commit


def get_now() -> datetime.datetime:
    now = datetime.datetime.utcnow()
    return now


def create_crawler_dict_list():
    crawler_dict_list = [
        dict(
            dataset="taiwan_stock_price",
        ),
        dict(
            dataset="taiwan_futures_daily",
        ),
    ]
    return crawler_dict_list


#TODO: need to save the count for each dataset
def save_dataset_count_daily(
    monitor_date: str = datetime.datetime.today().strftime("%Y-%m-%d"),
):
    '''
    Steps:
    1) Calculate the dataset count in monitor_date
    2) Update the result into Monitor database
    '''

    table = "DatasetCountDaily"
    sql = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            dataset_name VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            count INT NOT NULL,
            monitor_query_time DATETIME NOT NULL,
            SYS_CREATE_TIME DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (dataset_name, date, monitor_query_time)
        );
        """
    mysql_monitor_conn = router.mysql_monitor_conn
    commit(sql, mysql_monitor_conn)



if __name__ == "__main__":
    _ = save_dataset_count_daily("2022-03-01")
