CI_COMMIT_SHORT_SHA := $(shell git rev-parse --short=8 HEAD)

# 建立 image
build-grafana-image:
	docker build -f grafana/Dockerfile -t linsamtw/class01_grafana:6.2 .

# 上傳 image 到 docker hub
push-grafana-image:
	docker push linsamtw/class01_grafana:6.2

# 建立 image
build-prometheus-image:
	docker build -f prometheus/Dockerfile -t linsamtw/class01_prometheus:6.2 .

# 上傳 image 到 docker hub
push-prometheus-image:
	docker push linsamtw/class01_prometheus:6.2

# 啟動 grafana
deploy-grafana:
	docker stack deploy -c grafana.yml grafana

# 啟動 prometheus
deploy-prometheus:
	docker stack deploy -c prometheus.yml prometheus

# 啟動 cadvisor
deploy-cadvisor:
	docker stack deploy -c cadvisor.yml cadvisor