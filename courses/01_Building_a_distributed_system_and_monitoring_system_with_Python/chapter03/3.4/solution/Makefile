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

# sent task
sent-taiwan-future-task:
	pipenv run python financialdata/producer.py taiwan_taifex_future_daily 2021-04-01 2021-04-12

# sent task
sent-taiwan-option-task:
	pipenv run python financialdata/producer.py taiwan_taifex_option_daily 2021-04-01 2021-04-12

# sent task
sent-taiwan-stock-institutional-investors-tpex-task:
	pipenv run python financialdata/producer.py taiwan_tpex_stock_institutional_investors_buy_sell 2021-04-01 2021-04-12

# sent task
sent-taiwan-stock-institutional-investors-twse-task:
	pipenv run python financialdata/producer.py taiwan_twse_stock_institutional_investors_buy_sell 2021-04-01 2021-04-12

# sent task
sent-taiwan-stock-margin-purchase-tpex-task:
	pipenv run python financialdata/producer.py taiwan_tpex_stock_margin_purchase_short_sale 2021-04-01 2021-04-12

# sent task
sent-taiwan-stock-margin-purchase-twse-task:
	pipenv run python financialdata/producer.py taiwan_twse_stock_margin_purchase_short_sale 2021-04-01 2021-04-12
