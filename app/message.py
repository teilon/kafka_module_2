from confluent_kafka.serialization import Serializer
from confluent_kafka.serialization import Deserializer


class Message:
    def __init__(self, user_id: int, message_id: int, title: str):
        self.user_id = user_id
        self.message_id = message_id
        self.title = title

    def __str__(self):
        return f"Message ({self.message_id}) by {self.user_id}: {self.title}"


class MessageSerializer(Serializer):
    def __call__(self, obj: Message, ctx=None):
        user_id_bytes = obj.user_id.to_bytes(4, byteorder="big")

        title_bytes = obj.title.encode("utf-8")
        title_size = len(title_bytes)
        title_size_bytes = title_size.to_bytes(4, byteorder="big")

        message_id_bytes = obj.message_id.to_bytes(4, byteorder="big")

        return (
            user_id_bytes + title_size_bytes + title_bytes + message_id_bytes
        )


class MessageDeserializer(Deserializer):
    def __call__(self, value: bytes, ctx=None):
        if value is None:
            return None
        user_id_bytes = value[0:4]
        user_id = int.from_bytes(user_id_bytes, byteorder="big")

        title_size = int.from_bytes(value[4:8], byteorder="big")
        title_bytes = value[8:8 + title_size]
        title = title_bytes.decode("utf-8")

        message_id_bytes = value[8 + title_size:12 + title_size]
        message_id = int.from_bytes(message_id_bytes, byteorder="big")

        return Message(user_id, message_id, title)
