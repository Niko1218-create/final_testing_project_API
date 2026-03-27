import pytest
import allure

# Данные для негативных тестов авторизации
AUTH_INVALID_DATA = [
    {"name": ""},  # Пустое имя
    {},  # Нет имени
]

# Данные для негативных тестов создания мема
MEME_INVALID_DATA = [
    {"text": "", "url": "https://example.com/test.jpg", "tags": ["test"], "info": {"author": "Test"}},
    {"text": "Test", "url": "not-a-valid-url", "tags": ["test"], "info": {"author": "Test"}},
    {"url": "https://example.com/test.jpg", "tags": ["test"], "info": {"author": "Test"}},
    {"text": "Test", "tags": ["test"], "info": {"author": "Test"}},
]


@allure.story('Negative tests - Authorization')
@allure.title('Authorize with invalid data - should be 400')
@pytest.mark.parametrize('payload', AUTH_INVALID_DATA)
def test_auth_invalid_data(authorize_endpoint, payload):
    """Тест: авторизация с невалидными данными - всегда 400"""
    authorize_endpoint.create_token_with_payload(payload)
    authorize_endpoint.check_that_status_is_400()


@allure.story('Negative tests - Create meme')
@allure.title('Create meme with invalid data - should be 400')
@pytest.mark.parametrize('payload', MEME_INVALID_DATA)
def test_create_meme_invalid_data(create_meme_endpoint, token, payload):
    """Тест: создание мема с невалидными данными - всегда 400"""
    create_meme_endpoint.create_new_meme(payload, token)
    create_meme_endpoint.check_that_status_is_400()


@allure.story('Negative tests - No token')
class TestNoToken:
    """Тесты без токена авторизации - все ожидают 401"""

    @allure.title('Get all memes without token - should be 401')
    def test_get_memes_without_token(self, get_meme_endpoint):
        get_meme_endpoint.get_all_memes('')
        get_meme_endpoint.check_that_status_is_401()

    @allure.title('Create meme without token - should be 401')
    def test_create_meme_without_token(self, create_meme_endpoint):
        payload = {
            "text": "Test Meme",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        create_meme_endpoint.create_new_meme(payload, '')
        create_meme_endpoint.check_that_status_is_401()

    @allure.title('Get meme by ID without token - should be 401')
    def test_get_meme_by_id_without_token(self, get_meme_endpoint, meme_id):
        get_meme_endpoint.get_meme_by_id(meme_id, '')
        get_meme_endpoint.check_that_status_is_401()

    @allure.title('Update meme without token - should be 401')
    def test_update_meme_without_token(self, update_meme_endpoint, meme_id):
        payload = {
            "id": meme_id,
            "text": "Updated",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        update_meme_endpoint.update_meme_put(meme_id, payload, '')
        update_meme_endpoint.check_that_status_is_401()

    @allure.title('Delete meme without token - should be 401')
    def test_delete_meme_without_token(self, delete_meme_endpoint, meme_id):
        delete_meme_endpoint.delete_meme(meme_id, '')
        delete_meme_endpoint.check_that_status_is_401()


@allure.story('Negative tests - Non-existent resources')
class TestNonExistentResources:
    """Тесты несуществующих ресурсов - все ожидают 404"""

    @allure.title('Get non-existent meme - should be 404')
    def test_get_nonexistent_meme(self, get_meme_endpoint, token):
        get_meme_endpoint.get_meme_by_id(999999, token)
        get_meme_endpoint.check_that_status_is_404()

    @allure.title('Update non-existent meme - should be 404')
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

    @allure.title('Delete non-existent meme - should be 404')
    def test_delete_nonexistent_meme(self, delete_meme_endpoint, token):
        delete_meme_endpoint.delete_meme(999999, token)
        delete_meme_endpoint.check_that_status_is_404()


@allure.story('Negative tests - Invalid methods')
@allure.title('Use PATCH method - should be 405')
def test_patch_method_not_allowed(token, meme_id):
    """Тест: использование неподдерживаемого метода - ожидаем 405"""
    import requests

    response = requests.patch(
        f'http://memesapi.course.qa-practice.com/meme/{meme_id}',
        headers={'Authorization': token}
    )
    assert response.status_code == 405
