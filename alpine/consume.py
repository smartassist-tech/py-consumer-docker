import copy
import traceback
import os
from importlib import import_module

import pika


def _get_consumer_variables(name):
    p, m = name.rsplit('.', 1)

    mod = import_module(p)
    met = getattr(mod, m)

    return met


def get_rabbitmq_handler(handler, decode_body=True):
    decode_body = decode_body
    handler = handler

    def rabbitmq_handler(ch, method, properties, body):
        if decode_body:
            message = body.decode('utf-8')
        else:
            message = body
        handler(message=message, queue_kwargs={'ch': ch, 'method': method, 'properties': properties, 'body': body})

    return rabbitmq_handler


def make_channel_rabbitmq():
    CONSUMERS = _get_consumer_variables(os.environ['CONSUMER_IMPORT_PATH'])

    connection = pika.BlockingConnection(
        pika.URLParameters(os.environ['RABBITMQ_URL']))
    channel = connection.channel()

    for consumer in CONSUMERS:
        consumer_copy = copy.deepcopy(consumer)
        queue, handler = consumer_copy.pop('queue'), consumer_copy.pop('handler')
        decode_body = consumer_copy.pop('decode_body', True)

        channel.basic_consume(queue=queue,
                              on_message_callback=get_rabbitmq_handler(handler=handler, decode_body=decode_body),
                              **consumer_copy)

    return channel


while True:
    channel = make_channel_rabbitmq()

    try:
        channel.start_consuming()
    except:
        traceback.print_exc()

        try:
            channel.close()
        except:
            traceback.print_exc()
