# запуск
для запуска необходимо выполнить следующие шаги из корня:

* кластер kafka: docker-compose up -d
* продюсер и консьюмер: python app/main.py
* kafka-streams (faust): faust -A faust_app worker --loglevel=info

# описание сообщения (Message)
в проекте есть класс сообщения Message (с полями user_id: int message_id: int и title: str), где

user_id - рандомное число от 0 до 10

message_id - рандомное число от 0 до 10000

title - пара двух строковых значений, разделенных дефисом, из списка ("apple", "banana", "cherry", "date", "grape", "kiwi", "lemon", "mango", "orange", "pear", "plum", "strawberry", "watermelon")

# Логика работы
продюсер каждые 5 секунд генерирует и отправляет сообщения в топик 'messages'

faust_app реализует 3 функции агента
* automatic_filtration - автоматическая фильтрация по user_id, агент пишет в топик 'filtered_topic' сообщения где user_id не четные
* filtration_by_user_ignore_list - фильтрация по файлу user_ignore.txt, агент пишет в топик 'filtered_word_topic' сообщения где user_id не входит в список из user_ignore.txt
* filtration_by_word_ignore_list - фильтрация по файлу word_ignore.txt, агент пишет в топик 'clear_messages' сообщения где title не содержит слова из списока из word_ignore.txt

консьюмер подписан на топик 'clear_messages'
