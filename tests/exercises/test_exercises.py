from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema, GetExerciseResponseSchema, UpdateExerciseResponseSchema, UpdateExerciseRequestSchema
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ) -> None:
        """
        Тест проверяет создание задания через API.

        Шаги:
        1. Формируем запрос на создание задания с использованием данных из фикстуры курса
        2. Отправляем POST-запрос к /api/v1/exercises
        3. Проверяем статус код ответа (200 OK)
        4. Проверяем, что данные в ответе соответствуют запросу
        5. Валидируем JSON-схему ответа

        Args:
            exercises_client: Фикстура клиента для работы с заданиями
            function_course: Фикстура с данными созданного курса
        """
        # Формируем запрос на создание задания
        request = CreateExerciseRequestSchema(
            course_id=function_course.response.course.id
        )

        # Отправляем POST-запрос на создание задания
        response = exercises_client.create_exercise_api(request)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ) -> None:
        """
        Тест проверяет получение задания по ID.

        Шаги:
        1. Получаем ID задания из фикстуры function_exercise
        2. Отправляем GET-запрос к /api/v1/exercises/{exercise_id}
        3. Проверяем статус код ответа (200 OK)
        4. Проверяем, что данные в ответе соответствуют данным из фикстуры
        5. Валидируем JSON-схему ответа

        Args:
            exercises_client: Фикстура клиента для работы с заданиями
            function_exercise: Фикстура с данными созданного задания
        """
        # Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Отправляем GET-запрос на получение задания
        response = exercises_client.get_exercise_api(exercise_id)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные в ответе соответствуют данным из фикстуры
        assert_get_exercise_response(response_data, function_exercise.response)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ) -> None:
        """
        Тест проверяет обновление задания.

        Шаги:
        1. Получаем ID задания из фикстуры function_exercise
        2. Формируем запрос на обновление с новыми значениями
        3. Отправляем PATCH-запрос к /api/v1/exercises/{exercise_id}
        4. Проверяем статус код ответа (200 OK)
        5. Проверяем, что данные в ответе соответствуют запросу на обновление
        6. Валидируем JSON-схему ответа
        7. Проверяем, что задание действительно обновилось (опционально)

        Args:
            exercises_client: Фикстура клиента для работы с заданиями
            function_exercise: Фикстура с данными созданного задания
        """
        # Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id

        # Формируем запрос на обновление с новыми значениями
        request = UpdateExerciseRequestSchema()

        # Отправляем PATCH-запрос на обновление задания
        response = exercises_client.update_exercise_api(exercise_id, request)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные в ответе соответствуют запросу
        assert_update_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ) -> None:
        """
        Тест проверяет удаление задания.

        Шаги:
        1. Получаем ID задания из фикстуры function_exercise
        2. Отправляем DELETE-запрос к /api/v1/exercises/{exercise_id}
        3. Проверяем статус код ответа на удаление (200 OK)
        4. Пытаемся получить удаленное задание через GET-запрос
        5. Проверяем статус код ответа (404 Not Found)
        6. Проверяем, что в ответе содержится ошибка "Exercise not found"
        7. Валидируем JSON-схему ответа с ошибкой

        Args:
            exercises_client: Фикстура клиента для работы с заданиями
            function_exercise: Фикстура с данными созданного задания
        """
        # Получаем ID задания из фикстуры
        exercise_id = function_exercise.response.exercise.id
        print(f"\n📝 Исходное задание: ID={exercise_id}, название='{function_exercise.response.exercise.title}'")

        # Отправляем DELETE-запрос на удаление задания
        delete_response = exercises_client.delete_exercise_api(exercise_id)

        # Проверяем статус код ответа на удаление
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        print(f"✅ Задание {exercise_id} успешно удалено")

        # Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(exercise_id)

        # Проверяем статус код ответа (ожидаем 404 Not Found)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # Десериализуем JSON-ответ в модель InternalErrorResponseSchema
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # Проверяем, что в ответе содержится ошибка "Exercise not found"
        assert_exercise_not_found_response(get_response_data)

        # Валидируем JSON-схему ответа с ошибкой
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())


