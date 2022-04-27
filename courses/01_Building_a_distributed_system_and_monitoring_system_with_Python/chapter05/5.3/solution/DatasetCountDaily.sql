CREATE TABLE IF NOT EXISTS DatasetCountDaily (
    dataset_name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    count INT NOT NULL,
    monitor_query_time DATETIME NOT NULL,
    SYS_CREATE_TIME DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (dataset_name, date, monitor_query_time)
);