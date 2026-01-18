import pytest
import requests
import allure


class TestNegative:

    @allure.story('No token')
    @allure.title('Get all memes without token should fail')
    def test_get_memes_without_token(self):
        """Тест: получение мемов без токена должно завершиться ошибкой"""
        response = requests.get('http://memesapi.course.qa-practice.com/meme')
        assert response.status_code != 200, "Без токена должен быть ошибка"

    @allure.story('No token')
    @allure.title('Create meme without token should fail')
    def test_create_meme_without_token(self):
        """Тест: создание мема без токена должно завершиться ошибкой"""
        data = {
            "text": "Test Meme",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        response = requests.post(
            'http://memesapi.course.qa-practice.com/meme',
            json=data
        )
        assert response.status_code != 200, "Создание без токена должно быть ошибкой"

    # ========== ТЕСТЫ С НЕВАЛИДНЫМ ТОКЕНОМ ==========

    @allure.story('Invalid token')
    @allure.title('Get all memes with invalid token should fail')
    def test_get_memes_with_invalid_token(self, invalid_token):
        """Тест: получение мемов с невалидным токеном должно завершиться ошибкой"""
        headers = {'Authorization': invalid_token}
        response = requests.get(
            'http://memesapi.course.qa-practice.com/meme',
            headers=headers
        )
        assert response.status_code != 200, "С невалидным токеном должна быть ошибка"

    # ========== ТЕСТЫ НЕВАЛИДНЫХ ДАННЫХ ==========

    @pytest.mark.skip
    @allure.story('Invalid data')
    @allure.title('Create meme with empty text should fail')
    def test_create_meme_empty_text(self, token):
        """Тест: создание мема с пустым текстом должно завершиться ошибкой"""
        headers = {'Authorization': token}
        data = {
            "text": "",  # Пустой текст
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        response = requests.post(
            'http://memesapi.course.qa-practice.com/meme',
            json=data,
            headers=headers
        )
        assert response.status_code != 200, "Пустой текст должен вызывать ошибку"

    @pytest.mark.skip
    @allure.story('Invalid data')
    @allure.title('Create meme with invalid URL should fail')
    def test_create_meme_invalid_url(self, token):
        """Тест: создание мема с невалидным URL должно завершиться ошибкой"""
        headers = {'Authorization': token}
        data = {
            "text": "Test Meme",
            "url": "not-a-valid-url",  # Невалидный URL
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        response = requests.post(
            'http://memesapi.course.qa-practice.com/meme',
            json=data,
            headers=headers
        )
        assert response.status_code != 200, "Невалидный URL должен вызывать ошибку"

    @allure.story('Invalid data')
    @allure.title('Create meme missing required field should fail')
    def test_create_meme_missing_field(self, token):
        """Тест: создание мема без обязательного поля должно завершиться ошибкой"""
        headers = {'Authorization': token}
        data = {
            # Нет поля "text" - обязательное поле
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        response = requests.post(
            'http://memesapi.course.qa-practice.com/meme',
            json=data,
            headers=headers
        )
        assert response.status_code != 200, "Отсутствие обязательного поля должно вызывать ошибку"

    # ========== ТЕСТЫ НЕСУЩЕСТВУЮЩИХ РЕСУРСОВ ==========

    @allure.story('Non-existent resources')
    @allure.title('Get non-existent meme should return 404')
    def test_get_nonexistent_meme(self, token):
        """Тест: получение несуществующего мема должно возвращать 404"""
        headers = {'Authorization': token}
        non_existent_id = 999999
        response = requests.get(
            f'http://memesapi.course.qa-practice.com/meme/{non_existent_id}',
            headers=headers
        )
        assert response.status_code == 404, "Несуществующий мем должен возвращать 404"

    @allure.story('Non-existent resources')
    @allure.title('Update non-existent meme should return 404')
    def test_update_nonexistent_meme(self, token):
        """Тест: обновление несуществующего мема должно возвращать 404"""
        headers = {'Authorization': token}
        non_existent_id = 999999
        data = {
            "id": non_existent_id,
            "text": "Test",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"test": "test"}
        }
        response = requests.put(
            f'http://memesapi.course.qa-practice.com/meme/{non_existent_id}',
            json=data,
            headers=headers
        )
        assert response.status_code == 404, "Обновление несуществующего мема должно возвращать 404"

    @allure.story('Non-existent resources')
    @allure.title('Delete non-existent meme should return 404')
    def test_delete_nonexistent_meme(self, token):
        """Тест: удаление несуществующего мема должно возвращать 404"""
        headers = {'Authorization': token}
        non_existent_id = 999999
        response = requests.delete(
            f'http://memesapi.course.qa-practice.com/meme/{non_existent_id}',
            headers=headers
        )
        assert response.status_code == 404, "Удаление несуществующего мема должно возвращать 404"

    @allure.story('Non-existent resources')
    @allure.title('Update meme with wrong ID in body should fail')
    def test_update_meme_wrong_id(self, token, meme_id):
        """Тест: обновление мема с неправильным ID в теле запроса должно завершиться ошибкой"""
        headers = {'Authorization': token}
        data = {
            "id": 999999,  # Неправильный ID
            "text": "Test",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"test": "test"}
        }
        response = requests.put(
            f'http://memesapi.course.qa-practice.com/meme/{meme_id}',  # Правильный ID в URL
            json=data,
            headers=headers
        )
        assert response.status_code != 200, "Несовпадение ID в теле и URL должно вызывать ошибку"

    # ========== ТЕСТЫ ДВОЙНОГО УДАЛЕНИЯ ==========

    @allure.story('Double operations')
    @allure.title('Delete already deleted meme should return 404')
    def test_delete_already_deleted_meme(self, create_meme_endpoint, delete_meme_endpoint, token):
        """Тест: удаление уже удаленного мема должно возвращать 404"""
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
        assert delete_meme_endpoint.response.status_code == 200

        # Пытаемся удалить второй раз
        delete_meme_endpoint.delete_meme(meme_to_delete, token)
        assert delete_meme_endpoint.response.status_code == 404, "Второе удаление должно возвращать 404"