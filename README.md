## Первый запуск

1) Сформируй виртуальное Python-окружение
2) Установи зависимости `pip install -r requirements.txt`
3) Установи pre-commit hook `pre-commit install`

## Запуск Docker
1) Создать docker контейнеры `docker-compose build`
2) Запуск `docker-compose up`

## Линтер

Конфигурация для flake8 находится в `setup.cfg`

Запуск flake8: `flake8`

Запуск isort: `isort .`

## Тестирование

Запуск: `pytest .`

## CI-CD

В GitHub actions настроен запуск линтера при событии push.