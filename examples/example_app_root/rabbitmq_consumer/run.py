import random


def message_handler(message, queue_kwargs):
    print('Message Consumed')
    print(message)

    channel = queue_kwargs['ch']  # Get underlying pika Rabbitmq channel

    toss = random.randint(0, 1)

    if toss:
        print('Message Success')
    else:
        print('Message Failure')


CONSUMERS = [
    {
        'queue': 'testing',  # You must pre create a queue with this name in RabbitMQ
        'handler': message_handler,
    },

]
