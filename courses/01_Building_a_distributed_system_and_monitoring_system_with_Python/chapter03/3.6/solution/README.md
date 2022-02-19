# Class

#### 啟動 rabbitmq
    make deploy-rabbitmq

#### install package
    make install-package

#### 建立 network
    make create-network

#### 建立 mysql volume
    make create-mysql-volume

#### 啟動 mysql
    make deploy-mysql

#### 啟動 celery - twse
    make run-worker-twse

#### 啟動 celery - tpex
    make run-worker-tpex

#### 啟動 celery - taifex
    make run-worker-taifex

#### sent taiwan-stock-price task
    make sent-taiwan-stock-price-task

#### sent taiwan-futures-daily task
    make sent-taiwan-futures-daily-task

#### 建立 dev 環境變數
    make gen-dev-env-variable

