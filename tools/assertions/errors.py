import allure

from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema, InternalErrorResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.logger import get_logger

logger = get_logger("ERRORS_ASSERTIONS")

@allure.step("Check validation error")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    """
    Проверяет, что объект ошибки валидации соответствует ожидаемому значению.

    :param actual: Фактическая ошибка.
    :param expected: Ожидаемая ошибка.
    :raises AssertionError: Если значения полей не совпадают.
    """
    logger.info("Check validation error")

    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")


@allure.step("Check validation error response")
def assert_validation_error_response(
        actual: ValidationErrorResponseSchema,
        expected: ValidationErrorResponseSchema
):
    """
    Проверяет, что объект ответа API с ошибками валидации (`ValidationErrorResponseSchema`)
    соответствует ожидаемому значению.

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    logger.info("Check validation error response")

    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)


@allure.step("Check internal error response")
def assert_internal_error_response(
        actual: InternalErrorResponseSchema,
        expected: InternalErrorResponseSchema
):
    """
    Функция для проверки внутренней ошибки. Например, ошибки 404 (File not found).

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    logger.info("Check internal error response")

    assert_equal(actual.details, expected.details, "details")


@allure.step("Check validation error response contains error {error_type} at {location}")
def assert_has_validation_error(
        actual: ValidationErrorResponseSchema,
        error_type: str,
        location: list[str],
        message: str | None = None
):
    """
    Проверяет, что среди ошибок валидации есть ошибка заданного типа в заданном месте запроса.
    Не требует точного совпадения input/ctx, поэтому подходит для типовых проверок (missing, uuid_parsing и т.д.).

    :param actual: Фактический ответ API с ошибками валидации.
    :param error_type: Ожидаемый тип ошибки (например, "missing", "string_too_long").
    :param location: Ожидаемое расположение ошибки (например, ["body", "title"]).
    :param message: Ожидаемое сообщение ошибки (если нужно проверить).
    :raises AssertionError: Если подходящей ошибки нет.
    """
    logger.info(f"Check validation error response contains error {error_type} at {location}")

    found = any(
        detail.type == error_type
        and detail.location == location
        and (message is None or detail.message == message)
        for detail in actual.details
    )
    assert found, (
        f'Validation error not found. '
        f'Expected: type="{error_type}", location={location}, message={message}. '
        f'Actual: {[(d.type, d.location, d.message) for d in actual.details]}'
    )


@allure.step("Check not authenticated response")
def assert_not_authenticated_response(actual: InternalErrorResponseSchema):
    """
    Проверяет ответ на запрос без заголовка Authorization.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если сообщение об ошибке не совпадает.
    """
    logger.info("Check not authenticated response")

    assert_internal_error_response(actual, InternalErrorResponseSchema(details="Not authenticated"))


@allure.step("Check invalid token response")
def assert_invalid_token_response(actual: InternalErrorResponseSchema):
    """
    Проверяет ответ на запрос с невалидным или просроченным токеном.

    :param actual: Фактический ответ API.
    :raises AssertionError: Если сообщение об ошибке не совпадает.
    """
    logger.info("Check invalid token response")

    assert_internal_error_response(actual, InternalErrorResponseSchema(details="Invalid or expired token"))
