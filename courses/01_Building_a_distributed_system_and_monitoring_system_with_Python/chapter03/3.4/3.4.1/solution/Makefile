# 初始化 docker swarm
init-swarm:
	docker swarm init

# 啟動 rabbitmq
deploy-rabbitmq:
	docker stack deploy -c rabbitmq.yml rabbitmq

# 安裝相對應的 package
install-package:
	pipenv sync

# 啟動 celery
run-worker:
	pipenv run celery -A financialdata.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q celery

# sent task
sent-taiwan-stock-price-twse-task:
	pipenv run python financialdata/producer.py taiwan_twse_stock_price 2021-04-01 2021-04-12

# sent task
sent-taiwan-stock-price-tpex-task:
	pipenv run python financialdata/producer.py taiwan_tpex_stock_price 2021-04-01 2021-04-12
