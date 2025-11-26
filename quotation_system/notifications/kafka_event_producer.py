import json
from typing import Any

from confluent_kafka import Producer

producer_config = {"bootstrap.servers": "192.168.1.83:9092"}

producer = Producer(producer_config)


def send_event(entity: str, action: str, key: str, data: dict[str, Any]):

    key = str(key)  # force key to string
    payload = {"event_type": f"{entity}.{action}", "data": data}

    value_str = json.dumps(payload)

    producer.produce(topic=entity, key=key, value=value_str.encode("utf-8"))
    producer.flush()  # ensures delivery
