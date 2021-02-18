import json
import os

from kafka import KafkaConsumer, KafkaProducer


def deserializer(message):
    try:
        return json.loads(message.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        return message


config = {
    "consumer": {
        "default": {
            "auto_offset_reset": "latest",
            "enable_auto_commit": True,
            "group_id": os.getenv("KAFKA_GROUP_ID", "default"),
            "value_deserializer": deserializer,
            "session_timeout_ms": 60000,
            "heartbeat_interval_ms": 10000,
            "security_protocol": "PLAINTEXT",
        }
    },
    "producer": {
        "default": {
            "value_serializer": lambda x: json.dumps(x).encode("utf-8"),
        }
    },
}


def get_consumer(topics, bootstrap_servers):
    return KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        **config["consumer"]["default"],
    )


def get_producer(bootstrap_servers):
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        **config["producer"]["default"],
    )
