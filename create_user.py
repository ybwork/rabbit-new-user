import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

exchange_name = 'new_user'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct',
)

queue = 'create'

channel.queue_declare(
    queue=queue,
    durable=True,
)

channel.queue_bind(
    exchange=exchange_name,
    queue=queue,
    routing_key='create',
)


def callback(ch, method, properties, body):
    print('Создалась учётка для нового пользователя')

    exchange_name = 'base_router'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct'
    )

    channel.basic_publish(
        exchange=exchange_name,
        routing_key='base_router',
        body='user_created',
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )


channel.basic_consume(
    callback,
    queue=queue,
)

channel.start_consuming()

'''
    python create_user.py

'''
