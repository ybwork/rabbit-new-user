import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.7'))
channel = connection.channel()

exchange_name = 'add_user_to_group'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct'
)

queue_name = 'add'

channel.queue_declare(
    queue=queue_name,
    durable=True
)


channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key=queue_name,
)


def callback(channel, method, properties, body):
    print('Пользователь добавлен в группу')


channel.basic_consume(
    callback,
    queue=queue_name
)

channel.start_consuming()

# python add_user_to_group.py
