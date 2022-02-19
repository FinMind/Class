# 初始化 docker swarm
init-swarm:
	docker swarm init

# 啟動 rabbitmq
deploy-rabbitmq:
	docker stack deploy -c rabbitmq.yml rabbitmq

# 建立 network
create-network:
	docker network create --driver=overlay my_network

# 建立 mysql volume
create-mysql-volume:
	docker volume create mysql

# 啟動 rabbitmq
deploy-mysql:
	docker stack deploy -c mysql.yml mysql

# 安裝相對應的 package
install-package:
	pipenv sync

# 啟動 celery - twse
run-worker-twse:
	pipenv run celery -A financialdata.worker worker --loglevel=info --concurrency=1  --hostname=%h.twse -Q twse

# 啟動 celery - tpex
run-worker-tpex:
	pipenv run celery -A financialdata.worker worker --loglevel=info --concurrency=1  --hostname=%h.tpex -Q tpex

# 啟動 celery - taifex
run-worker-taifex:
	pipenv run celery -A financialdata.worker worker --loglevel=info --concurrency=1  --hostname=%h.taifex -Q taifex

# sent taiwan-stock-price task
sent-taiwan-stock-price-task:
	pipenv run python financialdata/producer.py taiwan_stock_price 2021-04-01 2021-04-12

# sent taiwan-futures-daily task
sent-taiwan-futures-daily-task:
	pipenv run python financialdata/producer.py taiwan_futures_daily 2021-04-01 2021-04-12

# 建立 dev 環境變數
gen-dev-env-variable:
	python genenv.py

# 建立 staging 環境變數
gen-staging-env-variable:
	VERSION=STAGING python genenv.py

# 建立 release 環境變數
gen-release-env-variable:
	VERSION=RELEASE python genenv.py