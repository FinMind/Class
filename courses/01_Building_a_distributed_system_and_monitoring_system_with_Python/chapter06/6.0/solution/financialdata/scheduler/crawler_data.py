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


def save_dataset_count_daily(
    monitor_date: str = datetime.datetime.today().strftime("%Y-%m-%d"),
):
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

    ret = []
    crawler_dict_list = create_crawler_dict_list()
    for crawler_dict in crawler_dict_list:
        dataset = crawler_dict.get("dataset")

        sql = f"""
            SELECT count(1) as nbr
            FROM `{dataset}`
            WHERE Date='{monitor_date}'
        """
        mysql_financialdata_conn = router.mysql_financialdata_conn
        count = query(sql=sql, mysql_conn=mysql_financialdata_conn)
        count = count[0][0]
        logger.info(f"{dataset} use mysql {monitor_date}:count {count}")

        monitor_query_time = get_now()
        ret.append([dataset, monitor_date, count, monitor_query_time])
    df = pd.DataFrame(ret, columns=["dataset_name", "date", "count", "monitor_query_time"])

    upload_data(df=df, table=table, mysql_conn=mysql_monitor_conn)


if __name__ == "__main__":
    _ = save_dataset_count_daily("2022-03-01")
