import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()


channel.exchange_declare(
    exchange='new_user',
    exchange_type='direct',
)

channel.basic_publish(
    exchange='new_user',
    routing_key='create',
    body='Появился новый пользователь',
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)

print('Нужно завести нового пользователя')

connection.close()

'''
    python task.py
'''
