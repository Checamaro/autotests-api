from http import HTTPStatus

import pytest

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize(
    "email_domain",
    [
        "mail.ru",
        "gmail.com",
        "example.com"
    ]
)
def test_create_user(email_domain: str, public_users_client: PublicUsersClient):
    email = fake.email(domain=email_domain)

    request = CreateUserRequestSchema(
        email=email,
        password=fake.password())
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user: UserFixture):
    response = private_users_client.get_user_me_api()

    assert_status_code(response.status_code, HTTPStatus.OK)

    response_data = GetUserResponseSchema.model_validate_json(response.text)

    validate_json_schema(response.json(), response_data.model_json_schema())

    assert_get_user_response(response_data, function_user.response)
