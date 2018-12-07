import pika


class Broker():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))

    # def
