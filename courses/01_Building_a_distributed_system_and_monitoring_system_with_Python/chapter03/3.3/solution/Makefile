
init-swarm:
	docker swarm init

deploy-rabbitmq:
	docker stack deploy -c rabbitmq.yml rabbitmq

install-package:
	pipenv sync

run-worker:
	pipenv run celery -A worker worker --loglevel=info

sent-task:
	pipenv run python producer.py
