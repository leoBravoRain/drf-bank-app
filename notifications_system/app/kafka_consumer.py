from aiokafka import AIOKafkaConsumer

KAFKA_BOOTSTRAP = "192.168.1.83:9092"  # Example for Docker/K8s internal networks


async def consume_messages():
    consumer = AIOKafkaConsumer(
        "account.created",
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="notificaction-service",
        enable_auto_commit=True,
    )

    await consumer.start()
    try:
        async for msg in consumer:

            # body = message.body.decode()
            # if not body:
            #     print("⚠️ Received empty message body, skipping...")
            #     return

            # payload = json.loads(body)
            # print("📩 Received email task:", payload)

            # email_payload = EmailPayload(
            #     from_='Eventia <hola@eventi-app.com>',
            #     to=['leo.bravo.rain@gmail.com'],
            #     subject= "New account created",
            #     html= "<h1>New account created </h1>",
            # )

            # send_email(email_payload)
            print(f"Received: {msg.value.decode()}")
    finally:
        await consumer.stop()
