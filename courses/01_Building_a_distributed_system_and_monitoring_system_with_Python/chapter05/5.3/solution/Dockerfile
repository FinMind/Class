# 由於 continuumio/miniconda3:4.3.27 中的 Debian
# 版本太舊，因此改用 ubuntu 系統
FROM ubuntu:18.04

# 系統升級、安裝 python
RUN apt-get update && apt-get install python3.6 -y && apt-get install python3-pip -y

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# env
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install package
RUN pip3 install pipenv==2020.6.2
RUN pipenv sync

# 在此 image, 使用 staging 環境變數
# 如果要用於 production 的 docker image
# 將此改成 VERSION=RELEASE 即可
RUN VERSION=STAGING python3 genenv.py

CMD ["/bin/bash"]