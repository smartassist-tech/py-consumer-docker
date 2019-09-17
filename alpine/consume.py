import copy
import traceback
import os
from importlib import import_module

import pika


def _get_consumer_variables(path):
    """
    Imports the CONSUMERS variable from the path definition. The consumer variable is defines as follows:

    Example:
        def test_handler(message, queue_kwargs):
            print('Consumer Receives')
            print(message)


        CONSUMERS = [

            {
                'queue': 'testing',
                'handler': test_handler,
                'decode_body': True,

                # Queue Specific variables
                'auto_ack': True
            }
        ]

    :param path: Path to the CONSUMERS variable. For example,
        `example_app.main.CONSUMERS` or `myapp.run.QUEUE_SETTINGS`
    :return:
    """
    p, m = path.rsplit('.', 1)

    mod = import_module(p)
    met = getattr(mod, m)

    return met


def get_rabbitmq_handler(handler, decode_body=True):
    """

    :param handler: The handler method to handle the message defined by the user. It is derived from the `CONSUMERS`
        variable defined above
    :param decode_body: Most queues return the body in byte format. By default the message is decoded and then returned.
    :return: Returns a closure as defined below. This decodes the body and calls the original handler.
    """
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
    """
    Connect to a RabbitMQ server and consume queues based on definition in the `CONSUMERS` variable.
    :return: Returns a `pika` channel.
    """
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
    # Make channel and consume continually
    # TODO: Add clearer exception handling
    # TODO: Add exception handler method hook defined by user
    channel = make_channel_rabbitmq()

    try:
        channel.start_consuming()
    except:
        traceback.print_exc()

        try:
            channel.close()
        except:
            traceback.print_exc()
