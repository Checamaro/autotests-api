from config import settings
import platform
import sys


def create_allure_environment_file():
    """
    Создает файл environment.properties с информацией об окружении
    для Allure отчета.
    """
    # Получаем базовые настройки из конфига
    base_items = [f'{key}={value}' for key, value in settings.model_dump().items()]

    # Добавляем информацию об ОС
    os_info = f'os_info={platform.system()}, {platform.release()}'

    # Добавляем информацию о версии Python
    python_version = f'python_version={sys.version}'

    # Создаем список из элементов в формате {key}={value}
    items = base_items + [os_info, python_version]

    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Создаем директорию для allure-results, если её нет
    settings.allure_results_dir.mkdir(exist_ok=True)

    # Открываем файл ./allure-results/environment.properties на чтение
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл
