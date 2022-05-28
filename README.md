## Первый запуск

1) Сформируй виртуальное Python-окружение
2) Установи зависимости `pip install -r requirements.txt`
3) Установи pre-commit hook `pre-commit install`

## Запуск Docker
1) Создать docker контейнеры `docker-compose build`
2) Запуск `docker-compose up`

## Kafka
1) Создание Kafka Topic после запуска docker compose
  `docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic movie_progress`

## Линтер

Конфигурация для flake8 находится в `setup.cfg`

Запуск flake8: `flake8`

Запуск isort: `isort .`

## Тестирование

Запуск: `pytest .`

## CI-CD

В GitHub actions настроен запуск линтера при событии push.
