import requests
import allure
from endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step('Delete meme by ID')
    def delete_meme(self, meme_id, token):
        headers = self.headers.copy()
        headers['Authorization'] = token

        self.response = requests.delete(
            f'{self.url}/meme/{meme_id}',
            headers=headers
        )
        return self.response
