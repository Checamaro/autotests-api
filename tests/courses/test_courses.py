from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity
from qase.pytest import qase

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, \
    GetCoursesQuerySchema, GetCoursesResponseSchema, GetCourseResponseSchema, CreateCourseResponseSchema, \
    CreateCourseRequestSchema
from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.files.files_client import FilesClient
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_update_course_response, assert_get_courses_response, \
    assert_create_course_response, assert_partial_update_course_response, assert_course_unchanged, \
    assert_course_not_found_response, assert_max_score_less_than_min_score_response, assert_course_not_in_courses, \
    assert_courses_empty, assert_get_course_response, assert_courses_match_by_id
from tools.assertions.errors import assert_has_validation_error, assert_not_authenticated_response, \
    assert_invalid_token_response
from tools.assertions.exercises import assert_exercise_not_found_response
from tools.assertions.files import assert_file_not_found_response
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
class TestCourses:
    @qase.id(1)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-1] Создание курса со всеми полями")
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(2)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-2] Создание курса без необязательных полей")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_without_optional_fields(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            max_score=None,
            min_score=None,
            estimated_time=None
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api(
            request.model_dump(by_alias=True, exclude={"max_score", "min_score", "estimated_time"})
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(3)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-3] Создание курса с явными null в maxScore, minScore, estimatedTime")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_null_optional_fields(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            max_score=None,
            min_score=None,
            estimated_time=None
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(4)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-4] Создание курса с title длиной 1")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_title_min_length(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            title=fake.string(1)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(5)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-5] Создание курса с title длиной 250")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_title_max_length(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            title=fake.string(250)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(9)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-9] Создание курса с description из 1 символа")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_description_min_length(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            description=fake.string(1)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(10)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-10] Создание курса с estimatedTime длиной 1")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_estimated_time_min_length(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            estimated_time=fake.string(1)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(11)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-11] Создание курса с estimatedTime длиной 50")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_estimated_time_max_length(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            estimated_time=fake.string(50)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(23)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-23] Создание курса, когда maxScore равен minScore")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_equal_max_and_min_score(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        score = fake.integer()
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            max_score=score,
            min_score=score
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(24)
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("[LMS-24] Создание курса с maxScore > 0 и minScore = null")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_course_with_null_min_score(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            min_score=None
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_create_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(27)
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.title("[LMS-27] Список курсов пользователя")
    @allure.severity(Severity.BLOCKER)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    def test_get_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_course: CourseFixture
    ):
        # 1. Формируем параметры запроса, передавая user_id
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        # 2. Отправляем GET-запрос на получение списка курсов
        response = courses_client.get_courses_api(query)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что список курсов соответствует ранее созданным курсам
        assert_get_courses_response(response_data, [function_course.response])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(28)
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.title("[LMS-28] Список из нескольких курсов")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    def test_get_several_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture,
            function_course: CourseFixture
    ):
        # 1. Создаём второй курс того же пользователя
        second_course = courses_client.create_course(
            CreateCourseRequestSchema(
                preview_file_id=function_file.response.file.id,
                created_by_user_id=function_user.response.user.id
            )
        )
        # 2. Формируем параметры запроса и запрашиваем список курсов
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        response = courses_client.get_courses_api(query)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что в списке оба курса
        assert_courses_match_by_id(response_data, [function_course.response, second_course])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(30)
    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.title("[LMS-30] Список курсов пользователя без курсов")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    def test_get_courses_of_user_without_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture
    ):
        # 1. Формируем параметры запроса для пользователя без курсов
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        # 2. Отправляем GET-запрос на получение списка курсов
        response = courses_client.get_courses_api(query)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что список пуст
        assert_courses_empty(response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(35)
    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("[LMS-35] Получение курса по id")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_course(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем GET-запрос на получение курса
        response = courses_client.get_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCourseResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 4. Проверяем, что данные курса соответствуют созданному курсу
        assert_get_course_response(response_data, function_course.response)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(41)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-41] Обновление курса: все поля")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        # 1. Формируем данные для обновления
        request = UpdateCourseRequestSchema()
        # 2. Отправляем запрос на обновление курса
        response = courses_client.update_course_api(function_course.response.course.id, request)
        # 3. Преобразуем JSON-ответ в объект схемы
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что данные в ответе соответствуют запросу
        assert_update_course_response(request, response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(42)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-42] Частичное обновление курса: только title")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_title_only(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema()
        updated_fields = {"title"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(43)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-43] Частичное обновление курса: только description")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_description_only(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema()
        updated_fields = {"description"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(44)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-44] Частичное обновление курса: только estimatedTime")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_estimated_time_only(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema()
        updated_fields = {"estimated_time"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(45)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-45] Обновление курса: title длиной 1")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_with_title_min_length(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema(title=fake.string(1))
        updated_fields = {"title"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(45)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-45] Обновление курса: title длиной 250")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_with_title_max_length(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema(title=fake.string(250))
        updated_fields = {"title"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(49)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-49] Обновление курса: estimatedTime длиной 50")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_with_estimated_time_max_length(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema(estimated_time=fake.string(50))
        updated_fields = {"estimated_time"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(52)
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("[LMS-52] Обновление курса, когда maxScore равен minScore")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_course_with_equal_max_and_min_score(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        score = fake.integer()
        # 1. Формируем данные для частичного обновления
        request = UpdateCourseRequestSchema(max_score=score, min_score=score)
        updated_fields = {"max_score", "min_score"}
        # 2. Отправляем PATCH-запрос только с выбранными полями
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include=updated_fields)
        )
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что изменились только переданные поля
        assert_partial_update_course_response(
            request,
            response_data,
            function_course.response.course,
            updated_fields
        )
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(61)
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("[LMS-61] Удаление курса")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_course(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем DELETE-запрос на удаление курса
        response = courses_client.delete_course_api(function_course.response.course.id)
        # 2. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 3. Запрашиваем удалённый курс
        get_response = courses_client.get_course_api(function_course.response.course.id)
        # 4. Проверяем, что курс больше не доступен
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

    @qase.id(62)
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("[LMS-62] После удаления курс недоступен")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_get_course_after_delete(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Удаляем курс
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        # 2. Проверяем, что курс удалён
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        # 3. Запрашиваем удалённый курс
        response = courses_client.get_course_api(function_course.response.course.id)
        # 4. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 5. Проверяем, что сервер вернул 404 и ошибку "Course not found"
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_course_not_found_response(response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(63)
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("[LMS-63] Удалённый курс пропадает из списка")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_deleted_course_not_in_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_course: CourseFixture
    ):
        # 1. Удаляем курс
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        # 2. Проверяем, что курс удалён
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        # 3. Запрашиваем список курсов пользователя
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        response = courses_client.get_courses_api(query)
        # 4. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        # 5. Проверяем статус код и отсутствие курса в списке
        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_course_not_in_courses(response_data, function_course.response.course.id)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(67)
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("[LMS-67] Удаление курса удаляет файл превью")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_course_deletes_preview_file(
            self,
            courses_client: CoursesClient,
            files_client: FilesClient,
            function_course: CourseFixture
    ):
        # 1. Удаляем курс
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        # 2. Проверяем, что курс удалён
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        # 3. Запрашиваем файл превью
        response = files_client.get_file_api(function_course.response.course.preview_file.id)
        # 4. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 5. Проверяем, что файл удалён (404, "File not found")
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_file_not_found_response(response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(68)
    @pytest.mark.xfail(reason="DELETE /courses/{id} не удаляет exercises курса: GET exercise после удаления возвращает 200 вместо 404 (issue будет заведён позже)", strict=True)
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.title("[LMS-68] Удаление курса удаляет exercises")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_course_deletes_exercises(
            self,
            courses_client: CoursesClient,
            exercises_client: ExercisesClient,
            function_course: CourseFixture,
            function_exercise: ExerciseFixture
    ):
        # 1. Удаляем курс
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        # 2. Проверяем, что курс удалён
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        # 3. Запрашиваем задание удалённого курса
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        # 4. Проверяем, что задание удалено (фактически сервер возвращает 200 и задание остаётся)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        # 5. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 6. Проверяем ошибку "Exercise not found" и схему ответа
        assert_exercise_not_found_response(response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
class TestCoursesNegative:
    @qase.id(6)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-6] Создание курса с title длиной 251")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_too_long_title(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            title=fake.string(251)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_too_long", ["body", "title"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(7)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-7] Создание курса с пустым title")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_empty_title(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            title=""
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_too_short", ["body", "title"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(8)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-8] Создание курса с пустым description")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_empty_description(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            description=""
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_too_short", ["body", "description"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(12)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-12] Создание курса с estimatedTime длиной 51")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_too_long_estimated_time(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            estimated_time=fake.string(51)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_too_long", ["body", "estimatedTime"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(13)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-13] Создание курса с пустым estimatedTime")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_empty_estimated_time(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            estimated_time=""
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_too_short", ["body", "estimatedTime"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(14)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-14] Создание курса без поля title")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_without_title(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api(
            request.model_dump(by_alias=True, exclude={"title"})
        )
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "missing", ["body", "title"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(15)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-15] Создание курса без поля description")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_without_description(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api(
            request.model_dump(by_alias=True, exclude={"description"})
        )
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "missing", ["body", "description"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(16)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-16] Создание курса без поля previewFileId")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_without_preview_file_id(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api(
            request.model_dump(by_alias=True, exclude={"preview_file_id"})
        )
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "missing", ["body", "previewFileId"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(17)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-17] Создание курса без поля createdByUserId")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_without_created_by_user_id(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api(
            request.model_dump(by_alias=True, exclude={"created_by_user_id"})
        )
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "missing", ["body", "createdByUserId"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(18)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-18] Создание курса с пустым телом запроса")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_empty_body(
            self,
            courses_client: CoursesClient
    ):
        # 1. Формируем некорректный запрос на создание курса

        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api({})
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "missing", ["body", "title"])
        assert_has_validation_error(response_data, "missing", ["body", "description"])
        assert_has_validation_error(response_data, "missing", ["body", "previewFileId"])
        assert_has_validation_error(response_data, "missing", ["body", "createdByUserId"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(19)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-19] Создание курса с невалидным uuid в previewFileId")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_invalid_preview_file_id(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=fake.string(10),
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "uuid_parsing", ["body", "previewFileId"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(20)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-20] Создание курса с невалидным uuid в createdByUserId")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_invalid_created_by_user_id(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=fake.string(10)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "uuid_parsing", ["body", "createdByUserId"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(21)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-21] Создание курса с неверными типами полей")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_invalid_field_types(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_raw_api(
            {
                **request.model_dump(by_alias=True),
                "title": fake.integer(),
                "maxScore": fake.string(5),
                "minScore": fake.string(5),
                "description": fake.integer(),
                "estimatedTime": fake.integer(),
                "previewFileId": fake.integer(),
                "createdByUserId": fake.integer()
            }
        )
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_type", ["body", "title"])
        assert_has_validation_error(response_data, "int_parsing", ["body", "maxScore"])
        assert_has_validation_error(response_data, "int_parsing", ["body", "minScore"])
        assert_has_validation_error(response_data, "string_type", ["body", "description"])
        assert_has_validation_error(response_data, "string_type", ["body", "estimatedTime"])
        assert_has_validation_error(response_data, "uuid_type", ["body", "previewFileId"])
        assert_has_validation_error(response_data, "uuid_type", ["body", "createdByUserId"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(22)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-22] Создание курса, когда maxScore меньше minScore")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_course_with_max_score_less_than_min_score(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_file: FileFixture
    ):
        # 1. Формируем некорректный запрос на создание курса
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id,
            max_score=fake.integer(1, 10),
            min_score=fake.integer(50, 100)
        )
        # 2. Отправляем POST-запрос на создание курса
        response = courses_client.create_course_api(request)
        # 3. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 4. Проверяем, что сервер вернул 422
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 5. Проверяем содержимое ошибки валидации
        assert_max_score_less_than_min_score_response(response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(31)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-31] Список курсов без параметра userId")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_get_courses_without_user_id(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.get_courses_raw_api({})
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "missing", ["query", "userId"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(32)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-32] Список курсов с невалидным userId")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_get_courses_with_invalid_user_id(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.get_courses_api(GetCoursesQuerySchema(user_id=fake.string(10)))
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "uuid_parsing", ["query", "userId"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(36)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-36] Получение несуществующего курса")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_get_nonexistent_course(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.get_course_api(fake.uuid4())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        # 4. Проверяем содержимое ошибки
        assert_course_not_found_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(37)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-37] Получение курса с невалидным uuid в path")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_get_course_with_invalid_course_id(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.get_course_api(fake.string(10))
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "uuid_parsing", ["path", "course_id"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(40)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-40] Получение удалённого курса")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_get_deleted_course(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        response = courses_client.get_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        # 4. Проверяем содержимое ошибки
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        assert_course_not_found_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(46)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-46] Обновление курса: title длиной 251")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_too_long_title(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        request = UpdateCourseRequestSchema(title=fake.string(251))
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"title"})
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "string_too_long", ["body", "title"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(47)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-47] Обновление курса: пустой title")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_empty_title(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        request = UpdateCourseRequestSchema(title="")
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"title"})
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "string_too_short", ["body", "title"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(48)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-48] Обновление курса: пустой description")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_empty_description(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        request = UpdateCourseRequestSchema(description="")
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"description"})
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "string_too_short", ["body", "description"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(49)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-49] Обновление курса: estimatedTime длиной 51")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_too_long_estimated_time(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        request = UpdateCourseRequestSchema(estimated_time=fake.string(51))
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"estimated_time"})
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "string_too_long", ["body", "estimatedTime"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(50)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-50] Обновление курса: пустой estimatedTime")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_empty_estimated_time(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        request = UpdateCourseRequestSchema(estimated_time="")
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"estimated_time"})
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "string_too_short", ["body", "estimatedTime"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(51)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-51] Обновление курса: maxScore меньше minScore")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_max_score_less_than_min_score(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        request = UpdateCourseRequestSchema(
            max_score=fake.integer(1, 10),
            min_score=fake.integer(50, 100)
        )
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"max_score", "min_score"})
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_max_score_less_than_min_score_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(53)
    @pytest.mark.xfail(reason="PATCH /courses/{id} c title=null возвращает 500 Internal Server Error вместо 422 (issue будет заведён позже)", strict=True)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-53] Обновление курса: title = null")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_null_title(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем запрос с title = null
        request = UpdateCourseRequestSchema(title=None)
        # 2. Отправляем PATCH-запрос
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"title"})
        )
        # 3. Проверяем, что сервер вернул 422 (фактически 500 Internal Server Error)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_type", ["body", "title"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(54)
    @pytest.mark.xfail(reason="PATCH /courses/{id} c description=null возвращает 500 Internal Server Error вместо 422 (issue будет заведён позже)", strict=True)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-54] Обновление курса: description = null")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_null_description(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем запрос с description = null
        request = UpdateCourseRequestSchema(description=None)
        # 2. Отправляем PATCH-запрос
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            request.model_dump(by_alias=True, include={"description"})
        )
        # 3. Проверяем, что сервер вернул 422 (фактически 500 Internal Server Error)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Десериализуем JSON-ответ с ошибкой валидации
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 5. Проверяем содержимое ошибки валидации
        assert_has_validation_error(response_data, "string_type", ["body", "description"])
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(55)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-55] Обновление курса с неверными типами полей")
    @allure.severity(Severity.MINOR)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_invalid_field_types(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        response = courses_client.update_course_raw_api(
            function_course.response.course.id,
            {
                "title": fake.integer(),
                "maxScore": fake.string(5),
                "minScore": fake.string(5),
                "description": fake.integer(),
                "estimatedTime": fake.integer()
            }
        )
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "string_type", ["body", "title"])
        assert_has_validation_error(response_data, "int_parsing", ["body", "maxScore"])
        assert_has_validation_error(response_data, "int_parsing", ["body", "minScore"])
        assert_has_validation_error(response_data, "string_type", ["body", "description"])
        assert_has_validation_error(response_data, "string_type", ["body", "estimatedTime"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(56)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-56] Обновление курса с невалидным uuid в path")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_course_with_invalid_course_id(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.update_course_api(fake.string(10), UpdateCourseRequestSchema())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "uuid_parsing", ["path", "course_id"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(57)
    @pytest.mark.xfail(reason="PATCH /courses/{id} для несуществующего курса возвращает 500 Internal Server Error вместо 404 (issue будет заведён позже)", strict=True)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-57] Обновление несуществующего курса")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_nonexistent_course(
            self,
            courses_client: CoursesClient
    ):
        # 1. Формируем запрос на обновление
        request = UpdateCourseRequestSchema()
        # 2. Отправляем PATCH-запрос для курса со случайным uuid
        response = courses_client.update_course_api(fake.uuid4(), request)
        # 3. Проверяем, что сервер вернул 404 (фактически 500 Internal Server Error)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        # 4. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 5. Проверяем, что ошибка "Course not found"
        assert_course_not_found_response(response_data)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(64)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-64] Повторное удаление курса")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_delete_course_twice(
            self,
            courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос
        delete_response = courses_client.delete_course_api(function_course.response.course.id)
        response = courses_client.delete_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        # 4. Проверяем содержимое ошибки
        assert_status_code(delete_response.status_code, HTTPStatus.OK)
        assert_course_not_found_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(65)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-65] Удаление несуществующего курса")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_delete_nonexistent_course(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.delete_course_api(fake.uuid4())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        # 4. Проверяем содержимое ошибки
        assert_course_not_found_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(66)
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.title("[LMS-66] Удаление курса с невалидным uuid в path")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_delete_course_with_invalid_course_id(
            self,
            courses_client: CoursesClient
    ):
        # 1. Отправляем запрос
        response = courses_client.delete_course_api(fake.string(10))
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 4. Проверяем содержимое ошибки
        assert_has_validation_error(response_data, "uuid_parsing", ["path", "course_id"])
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.COURSES)
class TestCoursesSecurity:
    @qase.id(25)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-25] Создание курса без токена")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_create_course_no_token(
            self,
            unauthorized_courses_client: CoursesClient
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = unauthorized_courses_client.create_course_api(CreateCourseRequestSchema())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_not_authenticated_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(26)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-26] Создание курса с невалидным токеном")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_create_course_invalid_token(
            self,
            invalid_token_courses_client: CoursesClient
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = invalid_token_courses_client.create_course_api(CreateCourseRequestSchema())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_invalid_token_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(29)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-29] Изоляция списков курсов разных пользователей")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_get_courses_isolation_between_users(
            self,
            second_user_courses_client: CoursesClient,
            function_second_user: UserFixture,
            function_course: CourseFixture
    ):
        # 1. Формируем параметры запроса для второго пользователя (у него курсов нет)
        query = GetCoursesQuerySchema(user_id=function_second_user.response.user.id)
        # 2. Второй пользователь запрашивает свой список курсов
        response = second_user_courses_client.get_courses_api(query)
        # 3. Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)
        # 4. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # 5. Проверяем, что курсов первого пользователя в списке нет
        assert_courses_empty(response_data)
        assert_course_not_in_courses(response_data, function_course.response.course.id)
        # 6. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(33)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-33] Список курсов без токена")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_get_courses_no_token(
            self,
            unauthorized_courses_client: CoursesClient,
            function_user: UserFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = unauthorized_courses_client.get_courses_api(GetCoursesQuerySchema(user_id=function_user.response.user.id))
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_not_authenticated_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(34)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-34] Список курсов с невалидным токеном")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_get_courses_invalid_token(
            self,
            invalid_token_courses_client: CoursesClient,
            function_user: UserFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = invalid_token_courses_client.get_courses_api(GetCoursesQuerySchema(user_id=function_user.response.user.id))
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_invalid_token_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(38)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-38] Получение курса без токена")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_get_course_no_token(
            self,
            unauthorized_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = unauthorized_courses_client.get_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_not_authenticated_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(39)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-39] Получение курса с невалидным токеном")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_get_course_invalid_token(
            self,
            invalid_token_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = invalid_token_courses_client.get_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_invalid_token_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(58)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-58] Обновление курса без токена")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_update_course_no_token(
            self,
            unauthorized_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = unauthorized_courses_client.update_course_api(function_course.response.course.id, UpdateCourseRequestSchema())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_not_authenticated_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(59)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-59] Обновление курса с невалидным токеном")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_update_course_invalid_token(
            self,
            invalid_token_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = invalid_token_courses_client.update_course_api(function_course.response.course.id, UpdateCourseRequestSchema())
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_invalid_token_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(60)
    @pytest.mark.xfail(reason="PATCH /courses/{id} чужим пользователем возвращает 200 и изменяет курс вместо 403 (issue будет заведён позже)", strict=True)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-60] Обновление чужого курса другим пользователем")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_update_foreign_course(
            self,
            courses_client: CoursesClient,
            second_user_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Формируем данные для обновления
        request = UpdateCourseRequestSchema()
        # 2. Второй пользователь отправляет PATCH-запрос для курса первого пользователя
        response = second_user_courses_client.update_course_api(function_course.response.course.id, request)
        # 3. Проверяем, что доступ запрещён (фактически сервер возвращает 200 и меняет данные)
        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        # 4. Владелец запрашивает свой курс
        get_response = courses_client.get_course_api(function_course.response.course.id)
        get_response_data = GetCourseResponseSchema.model_validate_json(get_response.text)
        # 5. Проверяем, что данные курса не изменились
        assert_status_code(get_response.status_code, HTTPStatus.OK)
        assert_course_unchanged(get_response_data.course, function_course.response.course)

    @qase.id(69)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-69] Удаление курса без токена")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_delete_course_no_token(
            self,
            unauthorized_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = unauthorized_courses_client.delete_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_not_authenticated_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(70)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-70] Удаление курса с невалидным токеном")
    @allure.severity(Severity.NORMAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_delete_course_invalid_token(
            self,
            invalid_token_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Отправляем запрос без валидной авторизации
        response = invalid_token_courses_client.delete_course_api(function_course.response.course.id)
        # 2. Десериализуем JSON-ответ с ошибкой
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        # 3. Проверяем статус код ответа
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        # 4. Проверяем сообщение об ошибке
        assert_invalid_token_response(response_data)
        # 5. Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @qase.id(71)
    @pytest.mark.xfail(reason="DELETE /courses/{id} чужим пользователем возвращает 200 и удаляет курс вместо 403 (issue будет заведён позже)", strict=True)
    @allure.tag(AllureTag.SECURITY)
    @allure.story(AllureStory.SECURITY)
    @allure.title("[LMS-71] Удаление чужого курса другим пользователем")
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.SECURITY)
    def test_delete_foreign_course(
            self,
            courses_client: CoursesClient,
            second_user_courses_client: CoursesClient,
            function_course: CourseFixture
    ):
        # 1. Второй пользователь отправляет DELETE-запрос для курса первого пользователя
        response = second_user_courses_client.delete_course_api(function_course.response.course.id)
        # 2. Проверяем, что доступ запрещён (фактически сервер возвращает 200 и удаляет курс)
        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        # 3. Владелец запрашивает свой курс
        get_response = courses_client.get_course_api(function_course.response.course.id)
        get_response_data = GetCourseResponseSchema.model_validate_json(get_response.text)
        # 4. Проверяем, что курс не удалён и не изменился
        assert_status_code(get_response.status_code, HTTPStatus.OK)
        assert_course_unchanged(get_response_data.course, function_course.response.course)
