FROM smartassist/py-consumer:latest

ENV CONSUMER_IMPORT_PATH consumer.main.CONSUMERS

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./ /