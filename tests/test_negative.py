import pytest
import allure

from endpoints.endpoint import Endpoint

# Тестовые данные
AUTH_TEST_DATA = [
    ({"name": ""}, 200),  # API принимает пустое имя
    ({}, 400),  # API не принимает отсутствие имени
]

MEME_TEST_DATA = [
    ({"text": "", "url": "https://example.com/test.jpg", "tags": ["test"], "info": {"author": "Test"}}, 200),
    ({"text": "Test", "url": "not-a-valid-url", "tags": ["test"], "info": {"author": "Test"}}, 200),
    ({"url": "https://example.com/test.jpg", "tags": ["test"], "info": {"author": "Test"}}, 400),
    ({"text": "Test", "tags": ["test"], "info": {"author": "Test"}}, 400),
]


@allure.story('Negative tests - Authorization')
@allure.title('Authorize with invalid data')
@pytest.mark.parametrize('payload,expected_status', AUTH_TEST_DATA)
def test_auth_invalid_data(authorize_endpoint, payload, expected_status):
    """Тест: авторизация с невалидными данными"""
    # Создаем запрос
    authorize_endpoint.response = authorize_endpoint.session.post(
        f'{authorize_endpoint.url}/authorize',
        json=payload,
        headers=authorize_endpoint.headers
    )
    authorize_endpoint.json = authorize_endpoint.safe_get_json()

    # Проверяем статус
    authorize_endpoint.check_status(expected_status)

    # Если успешная авторизация, проверяем токен
    if expected_status == 200 and authorize_endpoint.json:
        authorize_endpoint.check_token_exists()


@allure.story('Negative tests - Create meme')
@allure.title('Create meme with invalid data')
@pytest.mark.parametrize('payload,expected_status', MEME_TEST_DATA)
def test_create_meme_invalid_data(create_meme_endpoint, token, payload, expected_status):
    """Тест: создание мема с невалидными данными"""
    create_meme_endpoint.create_new_meme(payload, token)
    create_meme_endpoint.check_status(expected_status)


@allure.story('Negative tests - Update meme')
@allure.title('Update meme with invalid data')
@pytest.mark.parametrize('payload,expected_status', MEME_TEST_DATA)
def test_update_meme_invalid_data(update_meme_endpoint, token, meme_id, payload, expected_status):
    """Тест: обновление мема с невалидными данными"""
    # Копируем payload и добавляем ID
    data = payload.copy()
    data['id'] = meme_id

    update_meme_endpoint.update_meme_put(meme_id, data, token)
    update_meme_endpoint.check_status(expected_status)


@allure.story('Negative tests - No token')
class TestNoToken:
    """Тесты без токена авторизации"""

    @allure.title('Get all memes without token')
    def test_get_memes_without_token(self, get_meme_endpoint):
        get_meme_endpoint.get_all_memes('')
        get_meme_endpoint.check_status(500)

    @allure.title('Create meme without token')
    def test_create_meme_without_token(self, create_meme_endpoint):
        payload = {
            "text": "Test Meme",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        create_meme_endpoint.create_new_meme(payload, '')
        create_meme_endpoint.check_that_status_is_401()

    @allure.title('Get meme by ID without token')
    def test_get_meme_by_id_without_token(self, get_meme_endpoint, meme_id):
        get_meme_endpoint.get_meme_by_id(meme_id, '')
        get_meme_endpoint.check_status(500)

    @allure.title('Update meme without token')
    def test_update_meme_without_token(self, update_meme_endpoint, meme_id):
        payload = {
            "id": meme_id,
            "text": "Updated",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        update_meme_endpoint.update_meme_put(meme_id, payload, '')
        update_meme_endpoint.check_status(500)

    @allure.title('Delete meme without token')
    def test_delete_meme_without_token(self, delete_meme_endpoint, meme_id):
        delete_meme_endpoint.delete_meme(meme_id, '')
        delete_meme_endpoint.check_status(500)


@allure.story('Negative tests - Non-existent resources')
class TestNonExistentResources:
    """Тесты несуществующих ресурсов"""

    @allure.title('Get non-existent meme')
    def test_get_nonexistent_meme(self, get_meme_endpoint, token):
        get_meme_endpoint.get_meme_by_id(999999, token)
        get_meme_endpoint.check_that_status_is_404()

    @allure.title('Update non-existent meme')
    def test_update_nonexistent_meme(self, update_meme_endpoint, token):
        payload = {
            "id": 999999,
            "text": "Test",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        update_meme_endpoint.update_meme_put(999999, payload, token)
        update_meme_endpoint.check_that_status_is_404()

    @allure.title('Delete non-existent meme')
    def test_delete_nonexistent_meme(self, delete_meme_endpoint, token):
        delete_meme_endpoint.delete_meme(999999, token)
        delete_meme_endpoint.check_that_status_is_404()


@allure.story('Negative tests - Invalid methods')
@allure.title('Use PATCH method')
def test_patch_method_not_allowed(token, meme_id):
    """Тест: использование неподдерживаемого метода"""
    import requests

    # Создаем объект Endpoint для проверки
    endpoint = Endpoint()
    headers = endpoint.headers.copy()
    headers['Authorization'] = token

    endpoint.response = requests.patch(f'{endpoint.url}/meme/{meme_id}', headers=headers)
    endpoint.json = endpoint.safe_get_json()

    endpoint.check_status(405)


@allure.story('Negative tests - Double operations')
@allure.title('Delete already deleted meme')
def test_delete_already_deleted_meme(create_meme_endpoint, delete_meme_endpoint, get_meme_endpoint, token):
    """Тест: двойное удаление мема"""
    # Создаем мем
    payload = {
        "text": "Meme to delete twice",
        "url": "https://example.com/delete.jpg",
        "tags": ["delete"],
        "info": {"author": "Tester"}
    }
    create_meme_endpoint.create_new_meme(payload, token)
    meme_to_delete = create_meme_endpoint.json['id']

    # Удаляем первый раз
    delete_meme_endpoint.delete_meme(meme_to_delete, token)
    delete_meme_endpoint.check_that_status_is_200()

    # Проверяем, что мем удален
    get_meme_endpoint.get_meme_by_id(meme_to_delete, token)
    get_meme_endpoint.check_that_status_is_404()

    # Пытаемся удалить второй раз
    delete_meme_endpoint.delete_meme(meme_to_delete, token)
    delete_meme_endpoint.check_that_status_is_404()

