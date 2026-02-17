from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema, GetExerciseResponseSchema, ExerciseSchema, UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema, GetExercisesResponseSchema
)
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response


def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
) -> None:
    """
    Проверяет, что ответ на создание задания соответствует данным из запроса.

    Args:
        request: Исходный запрос на создание задания
        response: Ответ API с данными созданного задания

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает
    """
    # Проверяем основные поля задания
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema) -> None:
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    Args:
        actual: Фактические данные задания (из ответа API)
        expected: Ожидаемые данные задания (из фикстуры)

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


def assert_get_exercise_response(
        get_response: GetExerciseResponseSchema,
        create_response: CreateExerciseResponseSchema
) -> None:
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.

    Args:
        get_response: Ответ API при запросе задания
        create_response: Ответ API при создании задания

    Raises:
        AssertionError: Если данные задания не совпадают
    """
    assert_exercise(get_response.exercise, create_response.exercise)


def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
) -> None:
    """
    Проверяет, что ответ на обновление задания соответствует данным из запроса.

    Args:
        request: Запрос на обновление задания
        response: Ответ API с обновленными данными задания

    Raises:
        AssertionError: Если хотя бы одно поле не совпадает
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

def assert_exercise_not_found_response(actual: InternalErrorResponseSchema) -> None:
    """
    Проверяет, что ответ на запрос несуществующего задания содержит ошибку "Exercise not found".

    Args:
        actual: Фактический ответ от API с ошибкой

    Raises:
        AssertionError: Если фактический ответ не соответствует ожидаемой ошибке
    """
    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)

def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercise_responses: list[CreateExerciseResponseSchema]
) -> None:
    """
    Проверяет, что ответ на получение списка заданий соответствует ответам на их создание.

    Args:
        get_exercises_response: Ответ API при запросе списка заданий
        create_exercise_responses: Список API ответов при создании заданий

    Raises:
        AssertionError: Если данные заданий не совпадают
    """
    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(
            get_exercises_response.exercises[index],
            create_exercise_response.exercise
        )
