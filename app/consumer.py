import asyncio

from confluent_kafka import Consumer

from message import MessageDeserializer


conf = {
    "bootstrap.servers": "127.0.0.1:9094",
    "group.id": "consumer-group",           # Уникальный идентификатор группы
    "auto.offset.reset": "latest",        # Начало чтения с самого начала (latest, earliest)
    "enable.auto.commit": True,             # Автоматический коммит смещений
    "session.timeout.ms": 6_000,            # Время ожидания активности от консьюмера
    # "fetch.min.bytes": 1024,                # Минимальный объём данных (в байтах)
}


async def run_consumer(topic_name: str):
    print(">>>> Starting pull consumer...")

    consumer = Consumer(conf)
    consumer.subscribe([topic_name])

    try:
        while True:
            msg = await asyncio.to_thread(consumer.poll, 10)

            if msg is None:
                continue
            if msg.error():
                print(f"Ошибка: {msg.error()}")
                continue

            deserializer = MessageDeserializer()
            message = deserializer(msg.value())
            print(
                f"Получено сообщение: {message} " +
                f"от пользователя {message.user_id}"
            )

            consumer.commit(asynchronous=False)
    finally:
        consumer.close()
        print(">>>> Closed pull consumer...")
