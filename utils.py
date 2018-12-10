import pika


class Broker():
    def __init__(self, host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.connection = connection
        self.channel = connection.channel()

    def create_exchange(self, name, type):
        self.channel.exchange_declare(
            exchange=name,
            exchange_type=type,
        )

    def send_task(self, exchange, route, body=''):
        self.channel.basic_publish(
            exchange='new_user',
            routing_key='create',
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def create_queue(self, name, exclusive=False):
        self.channel.queue_declare(
            queue=name,
            exclusive=exclusive,
            durable=True
        )

    def bind_queue_exchange(self, exchange, queue, route):
        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=route,
        )

    def bind_callback_queue(self, callback, queue):
        self.channel.basic_consume(callback, queue=queue)

    def start_infinity_process(self):
        self.channel.start_consuming()
