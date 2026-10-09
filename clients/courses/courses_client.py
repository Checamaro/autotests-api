from httpx import Response
import allure
from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from clients.public_http_builder import get_public_http_client
from clients.courses.courses_schema import (
    GetCoursesQuerySchema,
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    UpdateCourseRequestSchema
)
from tools.fakers import fake
from tools.routes import APIRoutes


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    @allure.step("Get courses")
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        """
        Метод получения списка курсов.

        :param query: Словарь с userId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(APIRoutes.COURSES, params=query.model_dump(by_alias=True))

    @allure.step("Get courses with raw query")
    def get_courses_raw_api(self, params: dict) -> Response:
        """
        Метод получения списка курсов с произвольными query-параметрами (например, без userId).

        :param params: Словарь query-параметров.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(APIRoutes.COURSES, params=params)

    @allure.step("Get course by id {course_id}")
    def get_course_api(self, course_id: str) -> Response:
        """
        Метод получения курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.COURSES}/{course_id}")

    @allure.step("Create course")
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """
        Метод создания курса.

        :param request: Словарь с title, maxScore, minScore, description, estimatedTime,
        previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    @allure.step("Create course with raw payload")
    def create_course_raw_api(self, payload: dict) -> Response:
        """
        Метод создания курса с произвольным телом запроса (для негативных кейсов:
        отсутствующие поля, неверные типы, пустое тело).

        :param payload: Словарь, отправляемый как JSON без какой-либо валидации.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.COURSES, json=payload)

    @allure.step("Update course by id {course_id}")
    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """
        Метод обновления курса.

        :param course_id: Идентификатор курса.
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"{APIRoutes.COURSES}/{course_id}", json=request.model_dump(by_alias=True))

    @allure.step("Update course by id {course_id} with raw payload")
    def update_course_raw_api(self, course_id: str, payload: dict) -> Response:
        """
        Метод обновления курса с произвольным телом запроса (частичное обновление, null, неверные типы).

        :param course_id: Идентификатор курса.
        :param payload: Словарь, отправляемый как JSON без какой-либо валидации.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"{APIRoutes.COURSES}/{course_id}", json=payload)

    @allure.step("Delete course by id {course_id}")
    def delete_course_api(self, course_id: str) -> Response:
        """
        Метод удаления курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.COURSES}/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))


def get_unauthorized_courses_client() -> CoursesClient:
    """
    Функция создаёт CoursesClient без заголовка Authorization (для проверки ответа 401).

    :return: CoursesClient без авторизации.
    """
    return CoursesClient(client=get_public_http_client())


def get_invalid_token_courses_client() -> CoursesClient:
    """
    Функция создаёт CoursesClient с невалидным Bearer-токеном (для проверки ответа 401).

    :return: CoursesClient с произвольным токеном.
    """
    return CoursesClient(client=get_public_http_client(headers={"Authorization": f"Bearer {fake.access_token()}"}))
