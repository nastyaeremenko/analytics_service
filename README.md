# Сервис аналитики онлайн-кинотеатра
## Описание
Проект позволяет с помощью API получать данные в режиме реального времени о просмотре фильмов пользователем в онлайн-кинотеатре, 
записывать полученные данные в БД, которая позволяет хранить и обрабатывать большой объем данных.
Затем аналитики могут подключить БД к BI системе и получать необходимые данные для вычисления показателей.

После запуска кода документацию по API можно посмотреть по ссылке: http://localhost/api/openapi

## Технологии
- Python 3.9 
- FastAPI 0.78.0 
- Kafka-python 2.0.2
- Clickhouse-driver 0.2.3
- Zookeeper 3.5

## Запуск проекта
### Подготовка к запуску

1) Сформируй виртуальное Python-окружение
2) Установи зависимости `pip install -r requirements.txt`
3) Установи pre-commit hook `pre-commit install`

### Запуск Docker
1) Создать docker контейнеры `docker-compose build`
2) Запуск `docker-compose up`

### Kafka
1) Создание Kafka Topic после запуска docker compose
  `docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic movie_progress`

### Mongodb
#### После создания контейнера нужно создать базу данных и коллекции
1) `docker exec -it ugc-mongodb bash`
2) `mongosh`
3) `use ugc`
4) `db.createCollection("review")`
5) `db.createCollection("rating")`
6) `db.createCollection("bookmark")`

### Линтер

Конфигурация для flake8 находится в `setup.cfg`

Запуск flake8: `flake8`

Запуск isort: `isort .`

## Тестирование

Запуск: `pytest .`

## CI-CD

В GitHub actions настроен запуск линтера при событии push.

## Авторы
Дмитрий Вохмин, Максим Кезиков, Анастасия Еременко