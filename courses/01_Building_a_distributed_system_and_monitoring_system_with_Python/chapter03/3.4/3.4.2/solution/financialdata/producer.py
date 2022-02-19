import importlib
import sys

from financialdata.tasks import crawler
from loguru import logger


def update(
    dataset: str,
    start_date: str,
    end_date: str,
):
    # 拿取每個爬蟲任務的參數列表，
    # 包含爬蟲資料的日期 date，例如 2021-04-10 的台股股價，
    # 資料來源 data_source，例如 twse 證交所、tpex 櫃買中心
    parameter_list = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "gen_task_paramter_list",
    )(
        start_date=start_date,
        end_date=end_date,
    )
    # 用 for loop 發送任務
    for parameters in parameter_list:
        logger.info(f"{dataset}, {parameters}")
        task = crawler.s(dataset=dataset, parameters=parameters)
        # queue 參數，可以指定要發送到特定 queue 列隊中
        task.apply_async(queue=parameters.get("data_source", ""))


if __name__ == "__main__":
    (
        dataset,
        start_date,
        end_date,
    ) = sys.argv[1:]
    update(dataset, start_date, end_date)
