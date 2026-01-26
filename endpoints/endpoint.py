import allure


class Endpoint:
    url = 'http://memesapi.course.qa-practice.com'
    response = None
    json = None
    headers = {'Content-type': 'application/json'}

    @allure.step('Check that response status is 200')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200

    @allure.step('Check that response status is 201')
    def check_that_status_is_201(self):
        assert self.response.status_code == 201

    @allure.step('Check that response status is 400')
    def check_that_status_is_400(self):
        assert self.response.status_code == 400

    @allure.step('Check that response status is 401')
    def check_that_status_is_401(self):
        assert self.response.status_code == 401

    @allure.step('Check that response status is 404')
    def check_that_status_is_404(self):
        assert self.response.status_code == 404

    @allure.step('Check that response status is 405')
    def check_that_status_is_405(self):
        assert self.response.status_code == 405

    @allure.step('Check that text is correct')
    def check_response_text_is_correct(self, expected_text):
        assert self.json['text'] == expected_text

    @allure.step('Check that URL is correct')
    def check_response_url_is_correct(self, expected_url):
        assert self.json['url'] == expected_url

    @allure.step('Check that tags are correct')
    def check_response_tags_are_correct(self, expected_tags):
        assert self.json['tags'] == expected_tags

    @allure.step('Check that info is correct')
    def check_response_info_is_correct(self, expected_info):
        assert self.json['info'] == expected_info

    @allure.step('Check that ID exists')
    def check_response_id_is_not_none(self):
        assert self.json['id'] is not None

    @allure.step('Check that meme ID matches')
    def check_meme_id_matches(self, expected_id):
        assert self.json['id'] == expected_id

    @allure.step('Check that token exists')
    def check_token_exists(self):
        assert 'token' in self.json

    @allure.step('Check that the answer is not empty')
    def check_that_the_answer_is_not_empty(self, get_meme_endpoint):
        assert get_meme_endpoint.json is not None
        assert isinstance(get_meme_endpoint.json, list)
        assert len(get_meme_endpoint.json) > 0

    @allure.step('Check that the meme has been deleted')
    def check_that_the_meme_has_been_deleted(self, get_meme_endpoint):
        assert get_meme_endpoint.response.status_code == 404, "После удаления мем должен возвращать 404"

    @allure.step('Check that field is missing')
    def check_field_is_missing(self, field_name):
        assert field_name not in self.json

    @allure.step('Check that response list is empty')
    def check_response_list_is_empty(self):
        """Проверяет, что JSON ответ - пустой список"""
        assert self.json == []
