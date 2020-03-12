FROM python:3.7-alpine

ENV TELEGRAM_BOT_TOKEN=""
ENV USE_PROXY="true"
ENV TELEGRAM_PROXY_IP=""
ENV TELEGRAM_PROXY_PORT=""
ENV PAGINATION=10

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]