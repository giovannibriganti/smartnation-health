FROM ubuntu:latest

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        locales \
        python3-pip \
        python3-yaml \
        rsyslog systemd systemd-cron sudo \
    && apt-get clean

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY / ./

CMD [ "streamlit", "run", "ui_chat_db.py" ]