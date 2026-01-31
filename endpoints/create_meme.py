import requests
import allure
from endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):
    meme_id = None

    @allure.step('Create new meme')
    def create_new_meme(self, payload, token):
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.post(f'{self.url}/meme', json=payload, headers=headers)
        self.json = self.safe_get_json()
        self.meme_id = self.json['id']
        return self.response
