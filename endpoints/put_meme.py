import requests
import allure
from endpoints.endpoint import Endpoint


class UpdateMeme(Endpoint):
    @allure.step('Update meme using PUT')
    def update_meme_put(self, meme_id, payload, token):
        headers = {'Authorization': token}

        self.response = requests.put(f'{self.url}/meme/{meme_id}', json=payload, headers=headers)
        self.json = self.safe_get_json()
        return self.response
