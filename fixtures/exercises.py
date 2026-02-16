import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
        exercises_client: ExercisesClient,
        function_course: CourseFixture
) -> ExerciseFixture:
    request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)

    response = exercises_client.create_exercise(request)

    return ExerciseFixture(request=request, response=response)