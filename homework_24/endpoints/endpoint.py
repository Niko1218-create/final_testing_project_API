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

    @allure.step('Check that token exists')
    def check_token_exists(self):

        assert 'token' in self.json

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


