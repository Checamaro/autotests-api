# QA-агент проекта autotests-api

## Контекст
- Тестируемое приложение: LMS API-сервер
  https://github.com/Nikita-Filonov/qa-automation-engineer-api-course
- Локально сервер поднимается на http://localhost:8000, Swagger: http://localhost:8000/docs,
  OpenAPI JSON: http://localhost:8000/openapi.json — это наш «источник требований».
- TMS: Qase, проект с кодом `LMS` (через MCP-сервер `qase`).
- Баг-трекер: GitHub Issues этого репозитория (через `gh` CLI), метки `bug`, `ai-triage`, `flaky`, `test-issue`.
- Язык общения и комментариев в коде — русский.

## Стек и структура
- Python 3.12, pytest, httpx, pydantic v2, pydantic-settings, Faker, allure-pytest, pytest-xdist.
- `clients/<entity>/<entity>_client.py` — клиент, наследник `APIClient`; методы `*_api` возвращают `httpx.Response`,
  каждый метод помечен `@allure.step(...)`. Маршруты — только из `tools/routes.py` (`APIRoutes`).
- `clients/<entity>/<entity>_schema.py` — Pydantic-схемы запросов/ответов (camelCase через alias, `by_alias=True`).
- `fixtures/<entity>.py` — фикстуры; новый модуль фикстур регистрировать в `conftest.py`.
- `tools/assertions/<entity>.py` — функции `assert_*`, помечены `@allure.step`, используют `tools/assertions/base.py`.
- `tools/fakers.py` — генерация данных. Хардкод тестовых данных запрещён.
- `tests/<entity>/test_<entity>.py` — класс `Test<Entity>`, маркеры `@pytest.mark.<entity>` и `@pytest.mark.regression`,
  allure: tag, epic, feature, story, title, severity, parent_suite, suite, sub_suite — по образцу `tests/courses/test_courses.py`.
- Шаблон теста: запрос (схема) → вызов клиента → `model_validate_json` → `assert_status_code`
  → `assert_*` по данным → `validate_json_schema`. Шаги нумеруются комментариями.

## Правила
- Каждый автотест связан с кейсом Qase: `@qase.id(N)` (из `qase.pytest`) и id в `@allure.title("[LMS-N] ...")`.
- Новые enum-значения allure — в `tools/allure/*.py`, новые маркеры — в `pytest.ini`.
- Никаких `time.sleep`, `print` (есть `tools/logger.py`), голых `assert` в тестах — только функции из `tools/assertions`.
- Перед коммитом: `pytest -m regression -n 2` должен быть зелёным, кроме тестов, которые падают из-за
  подтверждённого бага (они помечаются `@pytest.mark.xfail(reason="#<issue>", strict=True)`).
- Ветки: `ai/<коротко-о-задаче>`. Коммиты на русском, в стиле `test(courses): негативные кейсы создания курса`.
- В `main` напрямую не пушить — только через Pull Request.
- Ничего не создавать в Qase и GitHub Issues без моего явного «да» (кроме запуска в CI, где правила задаёт workflow).
- Токены (QASE_API_TOKEN, GH_TOKEN) никогда не выводить и не записывать в файлы репозитория (`.env` в git!).

## Команды
- Сервер: см. README тестового сервера; переменные окружения как в `.github/workflows/tests.yml`.
- Все тесты: `pytest -m regression --alluredir=allure-results -n 2`
- Сводка падений для анализа: `python tools/ai/summarize_allure.py allure-results`
- Отчёт: `allure serve allure-results`

## Конвейер агентов
requirements-analyst → test-designer → autotest-writer → run-triager.
Запуск всего конвейера: `/qa-pipeline <эндпоинт или сущность>`. Подробности в `.claude/agents/`.
