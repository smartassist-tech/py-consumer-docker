import os
import time

import docker
import pika

client = docker.from_env()


def test_rabbit_consumption():
    container_rabbit = client.containers.run('rabbitmq:alpine', ports={'5672': '5672'},
                                             name='rabbit', detach=True)
    time.sleep(12)
    print(container_rabbit.logs().decode('utf-8'))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare('testing')

    channel.basic_publish(exchange='', routing_key='testing', body='Hello World! From Producer')

    connection.close()

    docker_path = os.getcwd() + '/alpine'
    tag = 'docker_python_consumer_testimage'
    client.images.build(path=docker_path, tag=tag)
    container_consumer = client.containers.run(tag, name='consumer', network_mode='host', detach=True)
    time.sleep(12)
    logs: str = container_consumer.logs()
    logs = logs.decode('utf-8')
    print('\n\n\n\n')
    print(logs)
    assert 'Consumer Receives' in logs
    assert 'Hello World! From Producer' in logs

    container_rabbit.stop()
    container_consumer.stop()

    container_rabbit.remove()
    container_consumer.remove()
