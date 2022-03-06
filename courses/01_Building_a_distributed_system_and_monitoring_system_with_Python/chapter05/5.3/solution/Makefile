CI_COMMIT_SHORT_SHA := $(shell git rev-parse --short=8 HEAD)

# 初始化 docker swarm
init-swarm:
	docker swarm init

# 啟動 portainer
deploy-portainer:
	docker stack deploy -c portainer.yml por

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

# 建立 image
build-image:
	docker build -f Dockerfile -t linsamtw/class01_crawler:dev .

# 上傳 image 到 docker hub
push-image:
	docker push linsamtw/class01_crawler:dev

# 部屬爬蟲工人
deploy-crawler-worker:
	docker stack deploy -c crawler_worker.yml crawler_worker

# 部屬 scheduler
deploy-crawler-scheduler:
	docker stack deploy -c crawler_scheduler.yml crawler_scheduler

build-grafana-image:
	SHA=${CI_COMMIT_SHORT_SHA} docker-compose -f grafana.yml build --no-cache

# 啟動 grafana
deploy-grafana: build-grafana-image
	SHA=${CI_COMMIT_SHORT_SHA} docker stack deploy -c grafana.yml grafana