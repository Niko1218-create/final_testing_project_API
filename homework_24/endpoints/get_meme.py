import requests
from endpoints.endpoint import Endpoint
import allure


class GetMeme(Endpoint):
    @allure.step('Get all memes')
    def get_all_memes(self, token):
        headers = self.headers.copy()
        headers['Authorization'] = token
        self.response = requests.get(f'{self.url}/meme', headers=headers)
        self.json = self.response.json()

    @allure.step('Get meme by ID')
    def get_meme_by_id(self, meme_id, token):
        headers = {'Authorization': token}
        self.response = requests.get(f'{self.url}/meme/{meme_id}', headers=headers)
        self.json = self.response.json()
        return self.response
