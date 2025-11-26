import json
from typing import Any

from confluent_kafka import Producer

producer_config = {"bootstrap.servers": "192.168.1.83:9092"}

producer = Producer(producer_config)


def send_event(entity: str, action: str, key: str, data: dict[str, Any]):

    key = str(key)  # force key to string
    payload = {
        "event_type": entity + "." + action,
        "data": json.dumps(data).encode("utf-8"),  # Kafka expects bytes
    }

    producer.produce(topic=entity, key=key, value=str(payload))
    producer.flush()  # ensures delivery
