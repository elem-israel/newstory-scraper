import json
import os

from kafka import KafkaConsumer, KafkaProducer

config = {
    "consumer": {
        "default": {
            "auto_offset_reset": "earliest",
            "enable_auto_commit": True,
            "group_id": "my-group-id",
            "value_deserializer": lambda x: json.loads(x.decode("utf-8")),
        }
    },
    "producer": {
        "default": {"value_serializer": lambda x: json.dumps(x).encode("utf-8")}
    },
}

consumer = KafkaConsumer(
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
