# import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
# channel = connection.channel()

# channel.exchange_declare(
#     exchange='new_user',
#     exchange_type='direct',
# )

# channel.basic_publish(
#     exchange='new_user',
#     routing_key='create',
#     body='',
#     properties=pika.BasicProperties(
#         delivery_mode=2,
#     )
# )


import utils

broker = utils.Broker(host='127.0.0.1')

exchange_name = 'new_user'

broker.create_exchange(
    name=exchange_name,
    type='direct'
)

broker.send_task(
    exchange=exchange_name,
    route='create'
)

print('Нужно завести нового пользователя')

broker.connection.close()

'''
    python task.py
'''
