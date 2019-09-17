def test_handler(message, queue_kwargs):
    """

    :param message: This is the decoded message in string format.
    :param queue_kwargs: These are queue specific args. These depend on the queue library. They are passed to the
        queue library when a connection is made and a channel is created.
    :return:
    """
    print('Consumer Receives')
    print(message)

    # User code here


CONSUMERS = [

    {
        'queue': 'testing',
        'handler': test_handler,
        'decode_body': True,

        # Extra queue specific args
        'auto_ack': True
    }
]
