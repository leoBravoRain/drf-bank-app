import json

from confluent_kafka import Producer

producer_config = {"bootstrap.servers": "192.168.1.83:9092"}

producer = Producer(producer_config)


def send_event(topic: str, key: str, value: dict):

    key = str(key)  # force key to string
    value = json.dumps(value).encode("utf-8")  # Kafka expects bytes

    producer.produce(topic=topic, key=key, value=str(value))
    producer.flush()  # ensures delivery
