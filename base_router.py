import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.7'))
channel = connection.channel()

exchange_name = 'base_router'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct'
)

result = channel.queue_declare(
    exclusive=True,
    durable=True
)

queue_name = result.method.queue

channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key='base_router'
)


def callback(channel, method, properties, body):
    executed_event = body.decode('utf-8')

    if executed_event == 'user_created':
        exchange_name = 'inform_router'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct'
        )

        channel.basic_publish(
            exchange=exchange_name,
            routing_key='inform_router',
            body=executed_event,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    elif executed_event == 'informed_web_about_new_user':
        exchange_name = 'register_user_accounts'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='fanout'
        )

        channel.basic_publish(
            exchange=exchange_name,
            routing_key='',
            body='',
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    elif executed_event == 'user_accounts_created':
        exchange_name = 'inform_router'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct'
        )

        channel.basic_publish(
            exchange=exchange_name,
            routing_key='inform_router',
            body=executed_event,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    elif executed_event == 'informed_all_about_user_in_system':
        exchange_name = 'add_user_to_group'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct'
        )

        channel.basic_publish(
            exchange=exchange_name,
            routing_key='add',
            body='',
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )


channel.basic_consume(
    callback,
    queue=queue_name
)

channel.start_consuming()

# python base_router.py
