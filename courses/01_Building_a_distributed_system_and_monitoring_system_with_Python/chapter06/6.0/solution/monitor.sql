-- Monitor 指標一
SELECT B.dataset_name,
    B.date,
    B.count
FROM(
    SELECT dataset_name,
        max(monitor_query_time) as max_monitor_query_time
    FROM `DatasetCountDaily`
    WHERE count > 0 AND DATE(date) >= (NOW() - INTERVAL 7 DAY)
    GROUP BY dataset_name ) AS A
LEFT JOIN(
    SELECT dataset_name,
        monitor_query_time,
        date,
        count
    FROM `DatasetCountDaily`
    WHERE count > 0 AND DATE(date) >= (NOW() - INTERVAL 7 DAY)
  ) AS B
ON A.dataset_name=B.dataset_name
AND A.max_monitor_query_time=B.monitor_query_time

-- Monitor 指標二
SELECT dataset_name,
    monitor_query_time as time_sec,
    count
FROM `DatasetCountDaily`
WHERE DATE(date) >= (NOW() - INTERVAL 7 DAY)