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
	pipenv run celery -A worker worker --loglevel=info

# 發送 task 給 rabbitmq
sent-task:
	pipenv run python producer.py
