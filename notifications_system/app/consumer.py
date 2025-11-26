import json

import aio_pika

from .services.email_service import EmailPayload, send_email

# If running with docker-compose
# RABBITMQ_URL = "amqp://admin:admin@rabbitmq/"
# If running with kubernetes
RABBITMQ_URL = "amqp://admin:admin@host.minikube.internal/"


async def email_handler(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            body = message.body.decode()
            if not body:
                print("⚠️ Received empty message body, skipping...")
                return

            payload = json.loads(body)
            print("📩 Received email task:", payload)

            email_payload = EmailPayload(
                from_="Eventia <hola@eventi-app.com>",
                to=["leo.bravo.rain@gmail.com"],
                subject="New account created",
                html="<h1>New account created </h1>",
            )

            send_email(email_payload)

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(
                f"   Message body: {message.body.decode() if message.body else 'Empty'}"
            )
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            print(
                f"   Message body: {message.body.decode() if message.body else 'Empty'}"
            )


async def consume():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    channel = await connection.channel()
    queue = await channel.declare_queue("email_queue", durable=True)

    print("👂 FastAPI consumer listening on 'email_queue'...")
    await queue.consume(email_handler)

    # Keep the consumer running
    return connection
