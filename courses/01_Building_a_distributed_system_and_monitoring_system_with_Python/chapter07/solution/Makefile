PWD := $(shell pwd)

build-latest-image-tensorflow:
	docker build -f tensorflow.Dockerfile -t class01_crawler:tensorflow .

run-code:
	docker run -it --rm --mount type=bind,source=${PWD}/tmp,target=/tmp/ class01_crawler:tensorflow
