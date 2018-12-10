import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

exchange_name = 'register_user_accounts'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='fanout',
)

queue_name = sys.argv[1]

result = channel.queue_declare(
    queue=queue_name,
    durable=True,
)

channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
)


def callback(ch, method, properties, body):
    print('Пользователь зарегистрирован в {}'.format(sys.argv[1]))

    exchange_name = 'base_router'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct'
    )

    channel.basic_publish(
        exchange=exchange_name,
        routing_key='base_router',
        body=sys.argv[2],
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )


channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)

channel.start_consuming()

'''
    python register_user_accounts.py slack ""

    python register_user_accounts.py redmine ""
    
    python register_user_accounts.py gitlab user_accounts_created
'''
