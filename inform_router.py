import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.7'))
channel = connection.channel()

exchange_name = 'inform_router'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct'
)

queue_name = 'inform_router'

result = channel.queue_declare(
    queue=queue_name,
    durable=True
)


channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key='inform_router'
)


def callback(channel, method, properties, body):
    event_from_base_router = body.decode('utf-8')

    if event_from_base_router == 'user_created':
        exchange_name = 'inform'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='topic'
        )

        channel.basic_publish(
            exchange=exchange_name,
            routing_key='inform.new_user.all',
            body='',
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    elif event_from_base_router == 'user_accounts_created':
        exchange_name = 'inform'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='topic'
        )

        event_for_inform_workers = 'informed_all_about_user_in_system'
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='inform.user_in_system.all',
            body=event_for_inform_workers,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )


channel.basic_consume(
    callback,
    queue=queue_name
)

channel.start_consuming()

# python inform_router.py
