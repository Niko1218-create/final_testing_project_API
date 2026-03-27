import requests
import allure
from endpoints.endpoint import Endpoint


class NegativeEndpoint(Endpoint):

    @allure.step('Get all memes without token - should be 401')
    def get_all_memes_without_token_401(self):
        self.response = requests.get(f'{self.url}/meme')
        # Не пытаемся получить JSON - это HTML страница
        assert self.response.status_code == 401, f"Should be 401 without token, got {self.response.status_code}"

    @allure.step('Create meme without token - should be 401')
    def create_meme_without_token_401(self, payload):
        self.response = requests.post(f'{self.url}/meme', json=payload)
        assert self.response.status_code == 401, f"Should be 401 without token, got {self.response.status_code}"

    @allure.step('Get meme by ID without token - should be 401')
    def get_meme_by_id_without_token_401(self, meme_id):
        self.response = requests.get(f'{self.url}/meme/{meme_id}')
        assert self.response.status_code == 401, f"Should be 401 without token, got {self.response.status_code}"

    @allure.step('Update meme without token - should be 401')
    def update_meme_without_token_401(self, meme_id, payload):
        self.response = requests.put(f'{self.url}/meme/{meme_id}', json=payload)
        assert self.response.status_code == 401, f"Should be 401 without token, got {self.response.status_code}"

    @allure.step('Delete meme without token - should be 401')
    def delete_meme_without_token_401(self, meme_id):
        self.response = requests.delete(f'{self.url}/meme/{meme_id}')
        assert self.response.status_code == 401, f"Should be 401 without token, got {self.response.status_code}"

    @allure.step('Authorize with empty name - should be 400')
    def authorize_empty_name_400(self):
        payload = {"name": ""}
        self.response = requests.post(f'{self.url}/authorize', json=payload, headers=self.headers)
        # Тут может быть JSON, но нам важен только статус
        assert self.response.status_code == 400, f"Should be 400 with empty name, got {self.response.status_code}"

    @allure.step('Authorize without name - should be 400')
    def authorize_without_name_400(self):
        payload = {}
        self.response = requests.post(f'{self.url}/authorize', json=payload, headers=self.headers)
        assert self.response.status_code == 400, f"Should be 400 without name, got {self.response.status_code}"

    @allure.step('Create meme with empty text - should be 400')
    def create_meme_empty_text_400(self, token):
        payload = {
            "text": "",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.post(f'{self.url}/meme', json=payload, headers=headers)
        assert self.response.status_code == 400, f"Should be 400 with empty text, got {self.response.status_code}"

    @allure.step('Create meme with invalid URL - should be 400')
    def create_meme_invalid_url_400(self, token):
        payload = {
            "text": "Test Meme",
            "url": "not-a-valid-url",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.post(f'{self.url}/meme', json=payload, headers=headers)
        assert self.response.status_code == 400, f"Should be 400 with invalid URL, got {self.response.status_code}"

    @allure.step('Create meme without text - should be 400')
    def create_meme_without_text_400(self, token):
        payload = {
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.post(f'{self.url}/meme', json=payload, headers=headers)
        assert self.response.status_code == 400, f"Should be 400 without text, got {self.response.status_code}"

    @allure.step('Create meme without URL - should be 400')
    def create_meme_without_url_400(self, token):
        payload = {
            "text": "Test Meme",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.post(f'{self.url}/meme', json=payload, headers=headers)
        assert self.response.status_code == 400, f"Should be 400 without URL, got {self.response.status_code}"

    @allure.step('Update meme with empty text - should be 400')
    def update_meme_empty_text_400(self, token, meme_id):
        payload = {
            "id": meme_id,
            "text": "",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.put(f'{self.url}/meme/{meme_id}', json=payload, headers=headers)
        assert self.response.status_code == 400, f"Should be 400 with empty text, got {self.response.status_code}"

    @allure.step('Update meme with invalid URL - should be 400')
    def update_meme_invalid_url_400(self, token, meme_id):
        payload = {
            "id": meme_id,
            "text": "Test Meme",
            "url": "not-a-valid-url",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.put(f'{self.url}/meme/{meme_id}', json=payload, headers=headers)
        assert self.response.status_code == 400, f"Should be 400 with invalid URL, got {self.response.status_code}"

    @allure.step('Get non-existent meme - should be 404')
    def get_nonexistent_meme_404(self, token):
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.get(f'{self.url}/meme/999999', headers=headers)
        assert self.response.status_code == 404, f"Should be 404 for non-existent meme, got {self.response.status_code}"

    @allure.step('Update non-existent meme - should be 404')
    def update_nonexistent_meme_404(self, token):
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            "id": 999999,
            "text": "Test",
            "url": "https://example.com/test.jpg",
            "tags": ["test"],
            "info": {"author": "Test"}
        }
        self.response = requests.put(f'{self.url}/meme/999999', json=payload, headers=headers)
        assert self.response.status_code == 404, f"Should be 404 for non-existent meme, got {self.response.status_code}"

    @allure.step('Delete non-existent meme - should be 404')
    def delete_nonexistent_meme_404(self, token):
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.delete(f'{self.url}/meme/999999', headers=headers)
        assert self.response.status_code == 404, f"Should be 404 for non-existent meme, got {self.response.status_code}"

    @allure.step('Use PATCH method - should be 405')
    def use_patch_method_405(self, meme_id, token):
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.patch(f'{self.url}/meme/{meme_id}', headers=headers)
        assert self.response.status_code == 405, f"Should be 405 for PATCH method, got {self.response.status_code}"
