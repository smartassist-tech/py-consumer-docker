def test_handler(message, queue_kwargs):
    print('Consumer Receives')
    print(message)


CONSUMERS = [

    {
        'queue': 'testing',
        'handler': test_handler,
        'decode_body': True,

        'auto_ack': True
    }
]
