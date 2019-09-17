import random


def failure_message_handler(message, queue_kwargs):
    print('Message Failed')
    print(message)


def success_message_handler(message, queue_kwargs):
    print('Success Failed')
    print(message)


def message_handler(message, queue_kwargs):
    print('Message Consumed')
    print(message)

    channel = queue_kwargs['ch']  # Get underlying pika Rabbitmq channel

    toss = random.randint(0, 1)

    if toss:
        channel.queue_declare('test_success')
        channel.basic_publish(exchange='', routing_key='test_success', body=message)
    else:
        channel.queue_declare('test_failure')
        channel.basic_publish(exchange='', routing_key='test_failure', body=message)


CONSUMERS = [
    {
        'queue': 'testing',  # You must pre create a queue with this name in RabbitMQ
        'handler': message_handler,
    },
    {
        'queue': 'test_success',
        'handler': success_message_handler,
    },
    {
        'queue': 'test_failure',
        'handler': failure_message_handler,
    },
]
