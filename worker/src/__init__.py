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

consumers = {
    topic: KafkaConsumer(
        topic,
        bootstrap_servers=[
            f'{os.getenv("KAFKA_URL", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
        ],
        **config["consumer"]["default"],
        **config["consumer"].get(topic, {}),
    )
    for topic in os.environ["KAFKA_TOPICS"].split(",")
}

producers = {
    topic: KafkaProducer(
        bootstrap_servers=[
            f'{os.getenv("KAFKA_URL", "localhost")}:{os.getenv("KAFKA_PORT", "9092")}'
        ],
        **config["producer"]["default"],
        **config["producer"].get(topic, {}),
    )
    for topic in os.environ["KAFKA_TOPICS"].split(",")
}
