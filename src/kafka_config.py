import json
import os

from kafka import KafkaConsumer, KafkaProducer


def value_deserializer(message):
    try:
        return json.loads(message.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        return message


def key_deserializer(key):
    try:
        return key.decode("utf-8")
    except AttributeError:
        return key


config = {
    "consumer": {
        "default": {
            "auto_offset_reset": "latest",
            "enable_auto_commit": True,
            "group_id": os.getenv("KAFKA_GROUP_ID", "default"),
            "value_deserializer": value_deserializer,
            "key_deserializer": key_deserializer,
            "session_timeout_ms": 60000,
            "heartbeat_interval_ms": 10000,
            "security_protocol": "PLAINTEXT",
        }
    },
    "producer": {
        "default": {
            "value_serializer": lambda x: json.dumps(x).encode("utf-8"),
            "key_serializer": lambda x: x.encode("utf-8"),
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
