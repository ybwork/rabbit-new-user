import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.7'))
channel = connection.channel()

exchange_name = 'add_user_to_group'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct'
)

result = channel.queue_declare(
    queue='add_user_to_group',
    durable=True
)

queue_name = result.method.queue

channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key='add_user_to_group'
)


def callback(channel, method, properties, body):
    print('new user full register')


channel.basic_consume(
    callback,
    queue=queue_name
)

channel.start_consuming()

# python add_user_to_group.py
