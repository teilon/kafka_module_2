для запуска необходимо выполнить следующие шаги из корня:

для запуска клостера kafka:
    docker-compose up -d
для запуска продюсера и консьюмера:
    python app/main.py
для запуска kafka-streams (faust):
    faust -A faust_app worker --loglevel=info

в проекте есть класс сообщения Message (с полями user_id: int message_id: int и title: str)

продюсер каждые 5 секунд генерирует собщение Message, где
user_id - рандомное число от 0 до 10
message_id - рандомное число от 0 до 10000
title - пара двух строковых значений, разделенных дефисом, из списка ("apple", "banana", "cherry", "date", "grape", "kiwi", "lemon", "mango", "orange", "pear", "plum", "strawberry", "watermelon")

продюсер отправляет сообщения в топик 'messages'

faust_app реализует 3 функции агента
* automatic_filtration - автоматическая фильтрация по user_id, агент пишет в топик 'filtered_topic' сообщения где user_id не четные
* filtration_by_user_ignore_list - фильтрация по файлу user_ignore.txt, агент пишет в топик 'filtered_word_topic' сообщения где user_id не входит в список из user_ignore.txt
* filtration_by_word_ignore_list - фильтрация по файлу word_ignore.txt, агент пишет в топик 'clear_messages' сообщения где title не содержит слова из списока из word_ignore.txt

консьюмер подписан на топик 'clear_messages'