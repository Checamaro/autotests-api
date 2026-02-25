from pydantic import BaseModel, HttpUrl, FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Self


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)


class TestDataConfig(BaseModel):
    image_png_file: FilePath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",  # Указываем, из какого файла читать настройки
        env_file_encoding="utf-8",  # Указываем кодировку файла
        env_nested_delimiter=".",  # Указываем разделитель для вложенных переменных
    )
    test_data: TestDataConfig
    http_client: HTTPClientConfig
    allure_results_dir: DirectoryPath

    # Добавили метод initialize
    @classmethod
    def initialize(cls) -> Self:  # Возвращает экземпляр класса Settings
        allure_results_dir = DirectoryPath("./allure-results")  # Создаем объект пути к папке
        allure_results_dir.mkdir(exist_ok=True)  # Создаем папку allure-results, если она не существует

        # Передаем allure_results_dir в инициализацию настроек
        return Settings(allure_results_dir=allure_results_dir)

settings = Settings.initialize()