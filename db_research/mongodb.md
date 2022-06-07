## Исследование баз данных

### MongoDB
Таблица лайков:

Key | Value                                |
--- |--------------------------------------|
user_uuid | 0a8e01de-bd11-4194-93dc-26309d641529 |
movie_uuid | f4d6d88b-8e28-4f0b-af70-d18d0b9df3f9 |
rating | 5                                    |

Таблица рецензий:

Key | Value                                |
--- |--------------------------------------|
text | review text                          |
first_name | First name                           |
last_name | Last name                            |
date | 2022-06-06                           |
user_uuid | 0a8e01de-bd11-4194-93dc-26309d641529 |
movie_uuid | f4d6d88b-8e28-4f0b-af70-d18d0b9df3f9 |
rating | 5                                    |

### Сравнение Postgresql и Mongodb

#### Загрузка новой записи
- Mongodb:
  - 4.57 ms  
  (Для таблицы содержащей 1 млн записей)
- Postgresql:
  -

#### Подсчет лайков, дислайков и средней оценки
- Mongodb:
  - 19.9 ms (2 млн)
- Postgresql:
  - 

#### Подсчет количества лайков и дислайков для рецензий на фильм
- Mongodb:
  - 39.9 ms (2 млн отзывов и 100 т рецензий)
- Postgresql:
  -

### Выводы

