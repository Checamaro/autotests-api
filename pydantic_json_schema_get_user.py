from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake

public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_api_response = public_users_client.create_user_api(create_user_request)
create_user_response_schema = CreateUserResponseSchema.model_json_schema()
validate_json_schema(
    instance=create_user_api_response.json(),
    schema=create_user_response_schema
)
create_user_response = CreateUserResponseSchema.model_validate_json(create_user_api_response.text)
user_id = create_user_response.user.id
auth_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
private_users_client = get_private_users_client(auth_user)
get_user_response = private_users_client.get_user_api(user_id)
get_user_schema = GetUserResponseSchema.model_json_schema()
validate_json_schema(
    instance=get_user_response.json(),
    schema=get_user_schema)
