import sys
import datetime

from financialdata.tasks import (
    crawler,
)


def gen_task_paramter_list(start_date: str, end_date: str):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    days = (end_date - start_date).days + 1
    date_list = [
        dict(crawler_date=str(start_date + datetime.timedelta(days=day)))
        for day in range(days)
    ]
    return date_list


def update(
    dataset: str,
    start_date: str,
    end_date: str,
):
    # 拿取每個爬蟲任務的參數列表，
    # 包含爬蟲資料的日期 date，例如 2021-04-10 的台股股價，
    parameter_list = gen_task_paramter_list(
        start_date=start_date,
        end_date=end_date,
    )
    # 用 for loop 發送任務
    for parameters in parameter_list:
        print(f"{dataset}, {parameters}")
        task = crawler.s(dataset, parameters)
        task.apply_async()


if __name__ == "__main__":
    (
        dataset,
        start_date,
        end_date,
    ) = sys.argv[1:]
    update(dataset, start_date, end_date)
