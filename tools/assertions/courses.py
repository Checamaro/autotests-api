from clients.courses.courses_schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, \
    GetCoursesResponseSchema, CreateCourseResponseSchema, CourseSchema, CreateCourseRequestSchema, \
    GetCourseResponseSchema
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response, assert_has_validation_error
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user
import allure
from tools.logger import get_logger

logger = get_logger("COURSES_ASSERTIONS")


@allure.step("Check create course response")
def assert_create_course_response(
        request: CreateCourseRequestSchema,
        response: CreateCourseResponseSchema
):
    """
    Проверяет, что ответ на создание курса соответствует данным из запроса.

    :param request: Исходный запрос на создание курса.
    :param response: Ответ API с данными созданного курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check create course response")

    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")

    assert_equal(response.course.preview_file.id, request.preview_file_id, "preview_file.id")

    assert_equal(response.course.created_by_user.id, request.created_by_user_id, "created_by_user.id")


@allure.step("Check update course response")
def assert_update_course_response(
        request: UpdateCourseRequestSchema,
        response: UpdateCourseResponseSchema
):
    """
    Проверяет, что ответ на обновление курса соответствует данным из запроса.

    :param request: Исходный запрос на обновление курса.
    :param response: Ответ API с обновленными данными курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check update course response")

    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check course")
def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Проверяет, что фактические данные курса соответствуют ожидаемым.

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check course")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    # Проверяем вложенные сущности
    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)


@allure.step("Check get courses response")
def assert_get_courses_response(
        get_courses_response: GetCoursesResponseSchema,
        create_course_responses: list[CreateCourseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.

    :param get_courses_response: Ответ API при запросе списка курсов.
    :param create_course_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    logger.info("Check get courses response")

    assert_length(get_courses_response.courses, create_course_responses, "courses")

    for index, create_course_response in enumerate(create_course_responses):
        assert_course(get_courses_response.courses[index], create_course_response.course)



@allure.step("Check partial update course response")
def assert_partial_update_course_response(
        request: UpdateCourseRequestSchema,
        response: UpdateCourseResponseSchema,
        original: CourseSchema,
        updated_fields: set[str]
):
    """
    Проверяет частичное обновление курса: переданные поля изменились, остальные остались прежними.

    :param request: Исходный запрос на обновление курса.
    :param response: Ответ API с обновленными данными курса.
    :param original: Данные курса до обновления.
    :param updated_fields: Имена полей схемы, которые отправлялись в запросе.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check partial update course response")

    for field in ("title", "max_score", "min_score", "description", "estimated_time"):
        expected = getattr(request, field) if field in updated_fields else getattr(original, field)
        assert_equal(getattr(response.course, field), expected, field)

    assert_equal(response.course.id, original.id, "id")


@allure.step("Check course is unchanged")
def assert_course_unchanged(actual: CourseSchema, expected: CourseSchema):
    """
    Проверяет, что данные курса не изменились (используется после отклонённых запросов).

    :param actual: Фактические данные курса.
    :param expected: Ожидаемые (исходные) данные курса.
    :raises AssertionError: Если данные отличаются.
    """
    logger.info("Check course is unchanged")

    assert_course(actual, expected)


@allure.step("Check course not found response")
def assert_course_not_found_response(actual: InternalErrorResponseSchema):
    """
    Проверяет ошибку, если курс не найден на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если ответ не соответствует ошибке "Course not found".
    """
    logger.info("Check course not found response")

    assert_internal_error_response(actual, InternalErrorResponseSchema(details="Course not found"))


@allure.step("Check max score less than min score response")
def assert_max_score_less_than_min_score_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет ошибку валидации, если maxScore меньше minScore.

    :param actual: Фактический ответ API с ошибками валидации.
    :raises AssertionError: Если ошибка не найдена.
    """
    logger.info("Check max score less than min score response")

    assert_has_validation_error(
        actual,
        error_type="value_error",
        location=["body"],
        message="Value error, max score should not be less than min score"
    )


@allure.step("Check course is not in courses list")
def assert_course_not_in_courses(response: GetCoursesResponseSchema, course_id: str):
    """
    Проверяет, что курса с указанным id нет в списке курсов.

    :param response: Ответ API со списком курсов.
    :param course_id: Идентификатор курса, который не должен присутствовать.
    :raises AssertionError: Если курс найден в списке.
    """
    logger.info("Check course is not in courses list")

    ids = [course.id for course in response.courses]
    assert course_id not in ids, f'Course "{course_id}" should not be in courses list. Actual ids: {ids}'


@allure.step("Check courses list is empty")
def assert_courses_empty(response: GetCoursesResponseSchema):
    """
    Проверяет, что список курсов пуст.

    :param response: Ответ API со списком курсов.
    :raises AssertionError: Если список не пуст.
    """
    logger.info("Check courses list is empty")

    assert_length(response.courses, [], "courses")


@allure.step("Check get course response")
def assert_get_course_response(
        get_course_response: GetCourseResponseSchema,
        create_course_response: CreateCourseResponseSchema
):
    """
    Проверяет, что ответ на получение курса соответствует ответу на его создание.

    :param get_course_response: Ответ API при запросе курса.
    :param create_course_response: Ответ API при создании курса.
    :raises AssertionError: Если данные курса не совпадают.
    """
    logger.info("Check get course response")

    assert_course(get_course_response.course, create_course_response.course)


@allure.step("Check courses list contains created courses")
def assert_courses_match_by_id(
        get_courses_response: GetCoursesResponseSchema,
        create_course_responses: list[CreateCourseResponseSchema]
):
    """
    Проверяет, что список курсов содержит ровно созданные курсы (без учёта порядка).

    :param get_courses_response: Ответ API при запросе списка курсов.
    :param create_course_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если количество или данные курсов не совпадают.
    """
    logger.info("Check courses list contains created courses")

    assert_length(get_courses_response.courses, create_course_responses, "courses")

    actual_by_id = {course.id: course for course in get_courses_response.courses}
    for create_course_response in create_course_responses:
        expected = create_course_response.course
        assert expected.id in actual_by_id, f'Course "{expected.id}" not found in courses list'
        assert_course(actual_by_id[expected.id], expected)
