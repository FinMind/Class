FROM tensorflow/tensorflow:latest-devel-py3

RUN apt-get update

RUN mkdir /solution
COPY . /solution/
WORKDIR /solution/

# install pyenv
RUN curl https://pyenv.run | bash &&\
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc &&\
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc &&\
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc &&\
    exec bash

# install pipenv
RUN /root/.pyenv/bin/pyenv install miniconda3-4.3.30
# install package
RUN pip install pipenv==2020.6.2 &&\
    pipenv sync

# selenium
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils &&\
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# chromedriver
RUN apt-get install chromium-chromedriver -y

# img
RUN mkdir /tmp/img

CMD ["/bin/bash"]
