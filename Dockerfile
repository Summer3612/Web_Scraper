FROM python:3.9


# Update the system and install firefox
RUN apt-get update 
RUN apt -y upgrade 
RUN apt-get install -y firefox-esr

# get the latest release version of firefox 
RUN latest_release=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep tag_name | sed -E 's/.*"([^"]+)".*/\1/') && \
    # Download the latest release of geckodriver
    wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz \
    # extract the geckodriver
    && tar -xvzf geckodriver-v0.31.0-linux64.tar.gz \
    # add executable permissions to the driver
    && chmod +x geckodriver \
    # Move gecko driver in the system path
    && mv geckodriver /usr/local/bin

COPY . . 

RUN pip install -r requirements.txt

CMD ["python", "main.py"]


# for chrome

# FROM --platform=linux/amd64 python:3.9 

# ENV CHROME_VERSION "google-chrome-stable"

# ENV DEBIAN_FRONTEND noninteractive

# RUN pip install --upgrade pip

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /backend

# RUN apt-get update \
#     && apt-get update && apt-get install -y gnupg2\
#     && apt-get install -y wget \
#     && apt-get install -y sudo\
#     && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
#     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
#     && apt-get -y update\
#     && apt-get install -y google-chrome-stable \
#     && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip\
#     && apt-get install -yqq unzip\
#     && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# COPY . .

# RUN pip install -r requirements.txt

# RUN apt update -y && apt install libgl1-mesa-glx sudo chromium chromium-driver -y

# CMD ["python", "main.py"]