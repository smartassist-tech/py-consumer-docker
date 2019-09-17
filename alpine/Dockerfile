FROM python:3-alpine
LABEL maintainer="Abhishek Jebaraj <abhishekjebaraj@outlook.com>"

ENV PROCESS_NUMBER 1
ENV RABBITMQ_URL "amqp://guest:guest@localhost:5672/%2F"
ENV CONSUMER_IMPORT_PATH example_app.main.CONSUMERS

RUN apk add --no-cache supervisor

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY supervisord.ini /etc/supervisor.d/supervisord.ini
COPY ./ /

CMD ["supervisord"]