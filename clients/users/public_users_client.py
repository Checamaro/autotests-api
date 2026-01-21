from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class PublicUserDict(TypedDict):
    """
    Описание структуры запроса для создания нового пользователя.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def create_user_api(self, request: PublicUserDict) -> Response:
        return self.post("/api/v1/users", json=request)