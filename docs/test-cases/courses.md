# Тест-кейсы: courses

Проект Qase `LMS`, suite `courses` (id 1). Заведено 71 кейс. Кандидаты на `xfail(strict=True)` отмечены «xfail?»: по коду сервера, запросами не подтверждено.
Исключены до уточнения требований (неоднозначные): TC-24, 26, 27, 28, 31, 36, 41, 47, 53, 62, 63, 66, 73, 85.

Общие предусловия: авторизованный пользователь с Bearer-токеном, загруженный файл превью; данные генерируются Faker.

| Qase ID | Эндпоинт | Название | Тип | Приоритет | Автоматизирован |
|---|---|---|---|---|---|
| LMS-1 | POST /courses | Создание курса со всеми полями | positive | High | `test_create_course` |
| LMS-2 | POST /courses | Создание без необязательных полей | positive | Medium | нет |
| LMS-3 | POST /courses | Явные null в maxScore, minScore, estimatedTime | positive | Medium | нет |
| LMS-4 | POST /courses | title длиной 1 | positive | Medium | нет |
| LMS-5 | POST /courses | title длиной 250 | positive | Medium | нет |
| LMS-6 | POST /courses | title длиной 251 (422) | negative | Medium | нет |
| LMS-7 | POST /courses | Пустой title (422) | negative | Medium | нет |
| LMS-8 | POST /courses | Пустой description (422) | negative | Medium | нет |
| LMS-9 | POST /courses | description из 1 символа | positive | Low | нет |
| LMS-10 | POST /courses | estimatedTime длиной 1 | positive | Low | нет |
| LMS-11 | POST /courses | estimatedTime длиной 50 | positive | Low | нет |
| LMS-12 | POST /courses | estimatedTime длиной 51 (422) | negative | Medium | нет |
| LMS-13 | POST /courses | Пустой estimatedTime (422) | negative | Medium | нет |
| LMS-14 | POST /courses | Отсутствует title (422) | negative | Medium | нет |
| LMS-15 | POST /courses | Отсутствует description (422) | negative | Medium | нет |
| LMS-16 | POST /courses | Отсутствует previewFileId (422) | negative | Medium | нет |
| LMS-17 | POST /courses | Отсутствует createdByUserId (422) | negative | Medium | нет |
| LMS-18 | POST /courses | Пустое тело (422) | negative | Medium | нет |
| LMS-19 | POST /courses | Невалидный uuid в previewFileId (422) | negative | Medium | нет |
| LMS-20 | POST /courses | Невалидный uuid в createdByUserId (422) | negative | Medium | нет |
| LMS-21 | POST /courses | Неверные типы полей (422) | negative | Medium | нет |
| LMS-22 | POST /courses | maxScore меньше minScore (422) | negative | High | нет |
| LMS-23 | POST /courses | maxScore равен minScore | positive | Medium | нет |
| LMS-24 | POST /courses | maxScore > 0, minScore = null | positive | Low | нет |
| LMS-25 | POST /courses | Создание без токена (401) | security | High | нет |
| LMS-26 | POST /courses | Создание с невалидным токеном (401) | security | High | нет |
| LMS-27 | GET /courses | Список курсов пользователя | positive | High | `test_get_courses` |
| LMS-28 | GET /courses | Список нескольких курсов | positive | Medium | нет |
| LMS-29 | GET /courses | Изоляция списков разных пользователей | security | High | нет |
| LMS-30 | GET /courses | Пользователь без курсов (пустой список) | positive | Medium | нет |
| LMS-31 | GET /courses | Без параметра userId (422) | negative | Medium | нет |
| LMS-32 | GET /courses | Невалидный userId (422) | negative | Medium | нет |
| LMS-33 | GET /courses | Список без токена (401) | security | High | нет |
| LMS-34 | GET /courses | Список с невалидным токеном (401) | security | High | нет |
| LMS-35 | GET /courses/{id} | Получение курса по id | positive | High | нет |
| LMS-36 | GET /courses/{id} | Несуществующий курс (404) | negative | High | нет |
| LMS-37 | GET /courses/{id} | Невалидный uuid в path (422) | negative | Medium | нет |
| LMS-38 | GET /courses/{id} | Без токена (401) | security | High | нет |
| LMS-39 | GET /courses/{id} | С невалидным токеном (401) | security | Medium | нет |
| LMS-40 | GET /courses/{id} | Удалённый курс (404) | negative | Medium | нет |
| LMS-41 | PATCH /courses/{id} | Обновление всех полей | positive | High | `test_update_course` |
| LMS-42 | PATCH /courses/{id} | Частичное обновление только title | positive | High | нет |
| LMS-43 | PATCH /courses/{id} | Частичное обновление только description | positive | Medium | нет |
| LMS-44 | PATCH /courses/{id} | Частичное обновление только estimatedTime | positive | Low | нет |
| LMS-45 | PATCH /courses/{id} | title длиной 1 и 250 | positive | Low | нет |
| LMS-46 | PATCH /courses/{id} | title длиной 251 (422) | negative | Medium | нет |
| LMS-47 | PATCH /courses/{id} | Пустой title (422) | negative | Medium | нет |
| LMS-48 | PATCH /courses/{id} | Пустой description (422) | negative | Medium | нет |
| LMS-49 | PATCH /courses/{id} | estimatedTime длиной 50 и 51 | negative | Low | нет |
| LMS-50 | PATCH /courses/{id} | Пустой estimatedTime (422) | negative | Low | нет |
| LMS-51 | PATCH /courses/{id} | maxScore меньше minScore, оба поля (422) | negative | High | нет |
| LMS-52 | PATCH /courses/{id} | maxScore равен minScore, оба поля | positive | Low | нет |
| LMS-53 | PATCH /courses/{id} | title = null (xfail?) | negative | High | нет |
| LMS-54 | PATCH /courses/{id} | description = null (xfail?) | negative | High | нет |
| LMS-55 | PATCH /courses/{id} | Неверные типы полей (422) | negative | Low | нет |
| LMS-56 | PATCH /courses/{id} | Невалидный uuid в path (422) | negative | Medium | нет |
| LMS-57 | PATCH /courses/{id} | Несуществующий курс (xfail?) | negative | High | нет |
| LMS-58 | PATCH /courses/{id} | Без токена (401) | security | High | нет |
| LMS-59 | PATCH /courses/{id} | С невалидным токеном (401) | security | Medium | нет |
| LMS-60 | PATCH /courses/{id} | Чужой курс другим пользователем (xfail?) | security | High | нет |
| LMS-61 | DELETE /courses/{id} | Удаление курса | positive | High | нет |
| LMS-62 | DELETE /courses/{id} | После удаления курс недоступен (404) | positive | High | нет |
| LMS-63 | DELETE /courses/{id} | Удалённый курс пропадает из списка | positive | Medium | нет |
| LMS-64 | DELETE /courses/{id} | Повторное удаление (404) | negative | High | нет |
| LMS-65 | DELETE /courses/{id} | Несуществующий курс (404) | negative | High | нет |
| LMS-66 | DELETE /courses/{id} | Невалидный uuid в path (422) | negative | Medium | нет |
| LMS-67 | DELETE /courses/{id} | Удаление курса удаляет файл превью | positive | Medium | нет |
| LMS-68 | DELETE /courses/{id} | Удаление курса удаляет exercises | positive | Medium | нет |
| LMS-69 | DELETE /courses/{id} | Без токена (401) | security | High | нет |
| LMS-70 | DELETE /courses/{id} | С невалидным токеном (401) | security | Medium | нет |
| LMS-71 | DELETE /courses/{id} | Чужой курс другим пользователем (xfail?) | security | High | нет |

Шаги и ожидаемые результаты — в самих кейсах Qase.
