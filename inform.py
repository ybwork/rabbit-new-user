import sys
import time
from datetime import datetime

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

exchange_name = 'inform'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='topic',
)

result = channel.queue_declare(
    exclusive=True,
    durable=True,
)

queue_name = result.method.queue

routes = sys.argv[1].split(', ')
for routing_key in routes:
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=routing_key,
    )


def callback(ch, method, properties, body):
    # time.sleep(3)

    # print(body.decode('utf-8'))

    # print('Время: {}'.format(datetime.now().time()))

    print(sys.argv[2])

    print('Уведомление отправлено {reciver} по {method}'.format(reciver=sys.argv[4], method=sys.argv[5]))

    event_from_inform_router = body.decode('utf-8')

    if event_from_inform_router == 'informed_user_web':
        exchange_name = 'base_router'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct'
        )

        executed_event = sys.argv[3]
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='base_router',
            body=executed_event,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    elif event_from_inform_router == 'informed_all_about_user_in_system':
        exchange_name = 'base_router'

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct'
        )

        executed_event = sys.argv[3]
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='base_router',
            body=executed_event,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

channel.basic_consume(
    callback,
    queue=queue_name,
)

channel.start_consuming()

'''    
    python inform.py "*.new_user.all, *.new_user.email, #.new_user.email.#" "email" "informed_web_about_new_user" "сектору web" "почте"
    python inform.py "*.new_user.all, *.new_user.sms, #.new_user.sms.#" "sms" "" "пользователю" "смс"

    
    python inform.py "*.user_in_system.all, *.user_in_system.email" "email" "informed_all_about_user_in_system" "сектору web" "почте"
    python inform.py "*.user_in_system.all, *.user_in_system.email" "email" "" "сектору 1C" "почте"
    python inform.py "*.user_in_system.all, *.user_in_system.email" "email" "" "сектору service" "почте"
    python inform.py "*.user_in_system.all, *.user_in_system.email" "email" "" "руководителю" "почте"
'''
