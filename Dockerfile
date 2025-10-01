FROM python:3.13-slim

LABEL authors="nikolay"

RUN apt update && apt upgrade -y
RUN apt install libpq-dev gcc -y && \
    apt install wget unzip curl -y && \
    apt install gnupg chromium -y && \
    apt install chromium-driver -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /application

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt &&  \
    rm -f requirements.txt

COPY main.py main.py
COPY db_connector.py db_connector.py
COPY celery_app.py celery_app.py
# COPY web_drivers/ ./web_drivers/
COPY collectors/ ./collectors/

# CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]