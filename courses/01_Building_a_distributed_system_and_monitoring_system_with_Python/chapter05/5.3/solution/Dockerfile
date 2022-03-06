FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

# 在此 image, 使用 staging 環境變數
# 如果要用於 production 的 docker image
# 將此改成 VERSION=RELEASE 即可
RUN VERSION=STAGING python genenv.py

# install package
RUN pip install pipenv && \
    pipenv sync

CMD ["/bin/bash"]