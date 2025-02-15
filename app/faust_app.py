import faust

from message import MessageDeserializer, MessageSerializer


# Описание модели данных
class Transaction(faust.Record):
    user_id: int
    message_id: int
    title: str


# Конфигурация Faust-приложения
app = faust.App(
    "simple-faust-app",
    broker="127.0.0.1:9094",
    value_serializer="raw",     # Работа с байтами (default: "json")
)

# Определение топика для входных данных
input_topic = app.topic("messages", key_type=str, value_type=bytes)

# Определение топика для выходных данных
filtered_topic = app.topic(
    "filtered_messages", key_type=str, value_type=bytes
)

filtered_word_topic = app.topic(
    "word_filtered_messages", key_type=str, value_type=bytes
)

output_topic = app.topic(
    "clear_messages", key_type=str, value_type=bytes
)

# @app.agent(input_topic)
# async def process_transactions(stream):
#     async for transaction in stream:
#         if transaction.user_id % 2 == 0:
#             await output_topic.send(value=transaction)


# Функция, реализующая потоковую обработку данных
@app.agent(input_topic)
async def automatic_filtration(stream):
    async for value in stream:
        # Обработка данных
        deserializer = MessageDeserializer()
        message = deserializer(value)

        if message.user_id % 2 == 0:
            continue

        serializer = MessageSerializer()
        processed_value = serializer(message)

        # Отправка обработанных данных в выходной топик
        await filtered_topic.send(value=processed_value)


@app.agent(filtered_topic)
async def filtration_by_user_ignore_list(stream):
    async for value in stream:
        # Получить список игнорируемых пользователей
        with open("user_ignore.txt", "r") as file:
            content = file.read()
            user_list = list(map(int, content.replace(' ', '').split(',')))

        # Обработка данных
        deserializer = MessageDeserializer()
        message = deserializer(value)

        if message.user_id in user_list:
            continue

        serializer = MessageSerializer()
        processed_value = serializer(message)

        # Отправка обработанных данных в выходной топик
        await filtered_word_topic.send(value=processed_value)


@app.agent(filtered_word_topic)
async def filtration_by_word_ignore_list(stream):
    async for value in stream:
        # Получить список игнорируемых пользователей
        with open("word_ignore.txt", "r") as file:
            content = file.read()
            word_list = content.replace(' ', '').split(',')

        # Обработка данных
        deserializer = MessageDeserializer()
        message = deserializer(value)

        is_filtered = False
        for x in word_list:
            if x in message.title:
                is_filtered = True
                break
        if is_filtered:
            continue

        serializer = MessageSerializer()
        processed_value = serializer(message)

        # Отправка обработанных данных в выходной топик
        await output_topic.send(value=processed_value)


if __name__ == '__main__':
    print(">>>> Starting Faust app")
    app.main()
