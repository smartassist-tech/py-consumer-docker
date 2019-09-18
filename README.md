Simple, dockerized and a generic python consumer for popular queues.

Currently it only supports RabbitMq but more will be added soon.

# Getting Started
Add a Dockerfile in your consumer project root.
```
FROM smartassist/py-consumer:latest

COPY ./ (Or any of your project folders) ./app

ENV PROCESS_NUMBER # (Optional)Default is 1
ENV RABBITMQ_URL # (Optional)Default is "amqp://guest:guest@localhost:5672/%2F"
ENV CONSUMER_IMPORT_PATH # (Optional)Default is example_app.main.CONSUMERS

```
For importing the Consumers, at the above CONSUMER_IMPORT_PATH, add the following
```
def test_handler(message, queue_kwargs): # Message is decoded by default. queue_kwargs are arguments from the queue you might require
    print('Consumer Receives {}'.format(message))
    

CONSUMERS = [
    {
        'queue': 'testing',
        'handler': test_handler, # Callable function to handle the message. Check examples for more.
        'decode_body' : True # Default True. Change it if you want the raw body
        # Queue specific variables
        'auto_ack': True
    }
]
```

Finally Run the container with

```
docker build -t "simple_consumer_demo:latest" .
docker run simple_consumer_demo:latest
```

# Settings

You can tweak the following environment variables for now.

###### PROCESS_NUMBER
Use it to have more consumer instances. Default 1

###### RABBITMQ_URL
This should include the full URL. Default is "amqp://guest:guest@localhost:5672/%2F"


###### CONSUMER_IMPORT_PATH
The default is app.main.CONSUMERS. But it can be changed in case your project uses other names

# Testing

```
Install docker and git clone
```
Then
```
pipenv install
sudo pipenv run pytest tests/
```
OR
```
pip install -r requirements.txt
sudo python -m pytest tests/
```

# Support
Reach out to us at:

abhishek@smartassist.tech

stallon@smartassist.tech

# Author
Abhishek Jebaraj

abhishekjebaraj@outlook.com
