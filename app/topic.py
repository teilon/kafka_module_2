from confluent_kafka.admin import AdminClient, NewTopic


conf = {"bootstrap.servers": "127.0.0.1:9094",}


def create_topic(topic_name: str):
    admin = AdminClient(conf)
    if admin.list_topics().topics.get(topic_name):
        print(f"Топик {topic_name} уже существует")
        return

    new_topic = NewTopic(
        topic_name,                            # Имя топика
        num_partitions=3,                      # Количество партиций
        replication_factor=2,                  # Фактор репликации
        config={"min.insync.replicas": "2"},   # Минимум 2 реплики должны подтвердить запись
    )
    admin.create_topics([new_topic])
    print(f"Топик {topic_name} создан успешно!")
