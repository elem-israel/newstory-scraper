import json
import os

from kafka import KafkaConsumer, KafkaProducer

config = {
    "consumer": {
        "default": {
            "auto_offset_reset": "latest",
            "enable_auto_commit": True,
            "group_id": os.getenv("KAFKA_GROUP_ID", "newstory-kafka-worker"),
            "value_deserializer": lambda x: json.loads(x.decode("utf-8")),
            "session_timeout_ms": 60000,
            "heartbeat_interval_ms": 10000,
        }
    },
    "producer": {
        "default": {"value_serializer": lambda x: json.dumps(x).encode("utf-8")}
    },
}


def get_consumer():
    return KafkaConsumer(
        *os.environ["KAFKA_TOPICS_LISTENER"].split(","),
        bootstrap_servers=[
            f'{os.getenv("KAFKA_HOST", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
        ],
        **config["consumer"]["default"],
    )


producer = KafkaProducer(
    bootstrap_servers=[
        f'{os.getenv("KAFKA_HOST", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
    ],
    **config["producer"]["default"],
)
