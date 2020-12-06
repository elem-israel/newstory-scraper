kafka-configs.sh --zookeeper $KAFKA_ZOOKEEPER_CONNECT --alter --topic newstory.tasks.newEntry --add-config retention.ms=1000
kafka-configs.sh --zookeeper $KAFKA_ZOOKEEPER_CONNECT --alter --topic newstory.tasks.newEntry --delete-config retention.ms
