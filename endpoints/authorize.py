import requests
import allure
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):
    token = None

    @allure.step('Create authorization token')
    def create_token(self, name='Nikolay'):
        """Позитивный тест - создание токена с валидным именем"""
        return self.create_token_with_payload({'name': name})

    @allure.step('Create token with payload')
    def create_token_with_payload(self, payload):
        """Универсальный метод для создания токена с любыми данными"""
        self.response = requests.post(f'{self.url}/authorize',
                                      json=payload,
                                      headers=self.headers)
        self.json = self.safe_get_json()
        if self.json and 'token' in self.json:
            self.token = self.json['token']
        return self.response

    @allure.step('Check token is alive')
    def check_token_alive(self, token):
        self.response = requests.get(f'{self.url}/authorize/{token}',
                                     headers=self.headers)
        self.json = self.safe_get_json()
        return self.response
