import os
import time

import docker
import pika

client = docker.from_env()


def _set_rabbitmq_container():
    """
    Run a RabbitMQ container and create a queue named `testing`.
    :return:
    """
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

    return container_rabbit


def _set_consumer_container(dockerfile_path, tag='docker_python_consumer_testimage'):
    """
    Run the consumer container and wait for a few messages to be consumed and printed
    :param dockerfile_path:
    :param tag:
    :return:
    """
    docker_path = os.getcwd() + dockerfile_path

    client.images.build(path=docker_path, tag=tag)
    container_consumer = client.containers.run(tag, name='consumer', network_mode='host', detach=True)
    time.sleep(12)

    return container_consumer


def test_rabbit_consumption():
    """
    Test the containerized consumers.

    1. We create the rabbitmq server and expose its main port.
    2. We declare a sample queue `testing` and push a message.
    3. The container is built and run. The container connects to the RabbitMQ Server, consumes the message prints the ouput.
    4. The test is successful if the message printed matches the message we had initially sent.
    :return:
    """

    container_rabbit = _set_rabbitmq_container()

    container_consumer = _set_consumer_container(dockerfile_path='/alpine')

    logs: str = container_consumer.logs()
    logs = logs.decode('utf-8')

    assert 'Consumer Receives' in logs
    assert 'Hello World! From Producer' in logs

    container_rabbit.stop()
    container_consumer.stop()

    container_rabbit.remove(force=True)
    container_consumer.remove(force=True)


def test_example_app_root_rabbit():
    container_rabbit = _set_rabbitmq_container()

    container_consumer = _set_consumer_container(dockerfile_path='/examples/example_app_root')

    logs: str = container_consumer.logs()
    logs = logs.decode('utf-8')

    assert 'Message Consumed' in logs
    assert 'Message Success' in logs or 'Message Failure' in logs

    container_rabbit.stop()
    container_consumer.stop()

    container_rabbit.remove()
    container_consumer.remove()
