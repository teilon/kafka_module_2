import asyncio
import random
import logging

from confluent_kafka import Producer

from message import Message, MessageSerializer


logger = logging.getLogger(__name__)
conf = {
    "bootstrap.servers": "127.0.0.1:9094",
    "acks": "all",  # Для синхронной репликации
    "retries": 3,   # Количество попыток при сбоях
}
words = [
    "apple", "banana", "cherry", "date", "grape", "kiwi", "lemon", "mango",
    "orange", "pear", "plum", "strawberry", "watermelon"
]


async def run_producer(topic_name: str):
    logger.info("Starting producer")
    print(">>>> Starting producer...")

    producer = Producer(conf)

    while True:
        message_id = random.randint(0, 10000)
        title = f"{random.choice(words)}-{random.choice(words)}"
        user_id = random.randint(0, 10)

        message = Message(user_id, message_id, title)
        serializer = MessageSerializer()
        value = serializer(message)

        producer.produce(topic=topic_name, key="key-1", value=value)
        await asyncio.to_thread(producer.flush)

        print(f"Отправленно сообщение: {message}")

        await asyncio.sleep(5)
