import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

exchange_name = 'new_user'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct',
)

channel.basic_publish(
    exchange=exchange_name,
    routing_key='create',
    body='',
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)

print('Нужно завести нового пользователя')

connection.close()

'''
    python task.py
'''
