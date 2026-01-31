import allure
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):
    token = None

    @allure.step('Create authorization token')
    def create_token(self, name='Nikolay'):
        body = {'name': name}
        self.response = self.session.post(f'{self.url}/authorize', json=body, headers=self.headers)
        self.json = self.safe_get_json()
        if self.json:
            self.token = self.json.get('token')
        return self.response

    @allure.step('Check token is alive')
    def check_token_alive(self, token):
        self.response = self.session.get(f'{self.url}/authorize/{token}', headers=self.headers)
        self.json = self.safe_get_json()
        return self.response
