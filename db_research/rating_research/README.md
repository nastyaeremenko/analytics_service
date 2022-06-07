## Исследование баз данных

### MongoDB

Таблица лайков:

Key         | Value                                |
---         |--------------------------------------|
user_uuid   | 0a8e01de-bd11-4194-93dc-26309d641529 |
movie_uuid  | f4d6d88b-8e28-4f0b-af70-d18d0b9df3f9 |
rating      | 5                                    |

Таблица рецензий:

Key         | Value                                |
---         |--------------------------------------|
text        | review text                          |
first_name  | First name                           |
last_name   | Last name                            |
date        | 2022-06-06                           |
user_uuid   | 0a8e01de-bd11-4194-93dc-26309d641529 |
movie_uuid  | f4d6d88b-8e28-4f0b-af70-d18d0b9df3f9 |
rating      | 5                                    |

### Postgres

Таблица лайков:

Key         | Value                                |
---         |--------------------------------------|
user_uuid   | 891f4dad-0099-4627-a1d1-28d8a459751f |
movie_uuid  | dc97ced0-8a69-45a4-82aa-cabb195cf8a6 |
rating      | 5                                    |

Таблица рецензий:

Key         | Value                                |
---         |--------------------------------------|
id          | dc97ced0-8a69-45a4-82aa-cabb195cf8a6 |
text_review | review text                          |
first_name  | First name                           |
last_name   | Last name                            |
date        | 2022-06-06                           |
user_uuid   | 0a8e01de-bd11-4194-93dc-26309d641529 |
movie_uuid  | f4d6d88b-8e28-4f0b-af70-d18d0b9df3f9 |


### Сравнение Postgresql и Mongodb

#### Загрузка новой записи

- Mongodb:
    - 4.57 ms  
      (Для таблицы содержащей 1 млн записей)
- Postgresql:
  - 17 ms
      (Для таблицы содержащей 1 млн записей)


#### Подсчет лайков, дислайков и средней оценки

- Mongodb:
  - 19.9 ms (2 млн)
- Postgresql:
  - подсчет лайков/дизлайков:
    - 120 ms (2 млн)
  - средняя оценка: 
    - 55.3 ms (2 млн)

#### Подсчет количества лайков и дислайков для рецензий на фильм

- Mongodb:
    - 39.9 ms (2 млн отзывов и 100 т рецензий)


### Выводы
По всем тестам MongoDB работает быстрее минимум в 5 раз, в связи с этим выбор в пользу MongoDB очевиден.

