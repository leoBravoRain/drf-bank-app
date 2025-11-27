import json

import pika
from django.conf import settings


def publish_email(message: dict):
    credentials = pika.PlainCredentials(
        settings.RABBITMQ["USER"], settings.RABBITMQ["PASSWORD"]
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ["HOST"],
            port=settings.RABBITMQ["PORT"],
            credentials=credentials,
        )
    )
    channel = connection.channel()

    # IMPORTANT: ensures queue exists!
    channel.queue_declare(queue=settings.RABBITMQ["QUEUE"], durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=settings.RABBITMQ["QUEUE"],
        body=json.dumps(message).encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )

    connection.close()
