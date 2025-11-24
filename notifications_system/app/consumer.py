import asyncio
import json

import aio_pika

RABBITMQ_URL = "amqp://admin:admin@rabbitmq/"


async def email_handler(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            body = message.body.decode()
            if not body:
                print("⚠️ Received empty message body, skipping...")
                return

            payload = json.loads(body)
            print("📩 Received email task:", payload)

            # simulate processing (send email, etc.)
            await asyncio.sleep(1)
            print("✔ Email processed")
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
