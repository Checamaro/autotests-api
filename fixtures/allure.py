import pytest

from tools.allure.environment import create_allure_environment_file


@pytest.fixture(scope='session', autouse=True)
def save_allure_environment_file():
    # До начала автотестов ничего не делаем
    yield  # Запускаются автотесты...
    # После завершения автотестов создаем файл environment.properties
    create_allure_environment_file()