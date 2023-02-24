FROM --platform=linux/amd64 python:3.9

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