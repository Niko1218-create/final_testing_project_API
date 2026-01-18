import requests
import allure
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):
    token = None

    @allure.step('Create authorization token')
    def create_token(self):
        body = {'name': 'Nikolay'}
        self.response = requests.post(f'{self.url}/authorize', json=body, headers=self.headers)

        self.json = self.response.json()
        self.token = self.json['token']
        return self.response

    @allure.step('Check token is alive')
    def check_token_alive(self, token):
        self.response = requests.get(f'{self.url}/authorize/{token}', headers=self.headers)
        return self.response

