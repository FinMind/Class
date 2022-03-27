CI_COMMIT_SHORT_SHA := $(shell git rev-parse --short=8 HEAD)

# 建立 image
build-grafana-image:
	docker build -f grafana/Dockerfile -t linsamtw/class06_grafana:6.1 .

# 上傳 image 到 docker hub
push-grafana-image:
	docker push linsamtw/class06_grafana:6.1

# 建立 image
build-prometheus-image:
	docker build -f prometheus/Dockerfile -t linsamtw/class06_prometheus:6.1 .

# 上傳 image 到 docker hub
push-prometheus-image:
	docker push linsamtw/class06_prometheus:6.1

# 啟動 grafana
deploy-grafana: build-grafana-image push-grafana-image
	SHA=${CI_COMMIT_SHORT_SHA} docker stack deploy -c grafana.yml grafana