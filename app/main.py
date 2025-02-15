import asyncio

from topic import create_topic
from consumer import run_consumer
from producer import run_producer


async def main():
    print(">>>> Starting app\n")

    create_topic('messages')
    create_topic('filtered_messages')
    create_topic('word_filtered_messages')
    create_topic('clear_messages')

    producer_task = asyncio.create_task(run_producer('messages'))
    consumer_task = asyncio.create_task(run_consumer('clear_messages'))

    await producer_task
    await consumer_task

    print(">>>> All tasks are complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(">>>> App stopped.")
