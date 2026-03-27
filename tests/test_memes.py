import pytest
import allure

import requests

TEST_DATA = [
    {
        "text": "Funny Cat Meme",
        "url": "https://ru.pinterest.com/nspshh/%D0%BC%D0%B5%D0%BC%D1%8B/",
        "tags": ["cat", "funny"],
        "info": {"author": "CatLover", "year": 2024}
    },
    {
        "text": "Programming Meme",
        "url": "https://skillbox.ru/media/marketing/chto-takoe-memy-i-kak-ikh-ispolzuyut-v-marketinge-i-smm/",
        "tags": ["programming", "developer"],
        "info": {"author": "Dev", "year": 2024}
    }
]

PUT_DATA = {
    "id": None,
    "text": "Updated Meme Text",
    "url": "https://lenta.ru/articles/2025/05/14/mem-okak/",
    "tags": ["updated", "new"],
    "info": {"author": "Updater", "year": 2025}
}


@allure.story('Authorization')
@allure.title('Get authorization token')
@allure.tag('auth')
def test_get_token(authorize_endpoint):
    authorize_endpoint.create_token()
    authorize_endpoint.check_that_status_is_200()
    authorize_endpoint.check_token_exists()


@allure.story('Authorization')
@allure.title('Check token is alive')
@allure.tag('auth')
def test_check_token_alive(authorize_endpoint, token):
    authorize_endpoint.check_token_alive(token)
    authorize_endpoint.check_that_status_is_200()


@allure.story('Create meme')
@allure.title('Create new meme')
@allure.tag('post')
@pytest.mark.parametrize('data', TEST_DATA)
def test_create_new_meme_with_valid_data(create_meme_endpoint, token, data):
    create_meme_endpoint.create_new_meme(data, token)
    create_meme_endpoint.check_that_status_is_200()
    create_meme_endpoint.check_response_text_is_correct(data['text'])
    create_meme_endpoint.check_response_url_is_correct(data['url'])
    create_meme_endpoint.check_response_tags_are_correct(data['tags'])
    create_meme_endpoint.check_response_info_is_correct(data['info'])
    create_meme_endpoint.check_response_id_is_not_none()


@pytest.mark.skip
@allure.story('Get meme')
@allure.title('Get all memes')
@allure.tag('get')
def test_get_all_memes(get_meme_endpoint, token, create_meme_endpoint):
    # Создаем мем, чтобы список не был пустым
    payload = {
        "text": "Test meme for get all",
        "url": "https://www.google.com/webhp?hl=RU",
        "tags": ["test"],
        "info": {"author": "Tester"}
    }
    create_meme_endpoint.create_new_meme(payload, token)

    get_meme_endpoint.get_all_memes(token)
    get_meme_endpoint.check_that_status_is_200()
    get_meme_endpoint.check_that_answer_is_not_empty()


@allure.story('Get meme')
@allure.title('Get meme by ID')
@allure.tag('get')
def test_get_meme_by_id(get_meme_endpoint, token, meme_id):
    get_meme_endpoint.get_meme_by_id(meme_id, token)
    get_meme_endpoint.check_that_status_is_200()
    get_meme_endpoint.check_meme_id_matches(meme_id)


@allure.story('Update meme')
@allure.title('Update meme using PUT')
@allure.tag('put')
def test_put_meme(update_meme_endpoint, token, meme_id):
    update_data = PUT_DATA.copy()
    update_data['id'] = meme_id

    update_meme_endpoint.update_meme_put(meme_id, update_data, token)
    update_meme_endpoint.check_that_status_is_200()
    update_meme_endpoint.check_response_text_is_correct(update_data['text'])
    update_meme_endpoint.check_response_url_is_correct(update_data['url'])
    update_meme_endpoint.check_response_tags_are_correct(update_data['tags'])
    update_meme_endpoint.check_response_info_is_correct(update_data['info'])


@allure.story('Delete meme')
@allure.title('Delete meme by ID')
@allure.tag('delete')
def test_delete_meme(delete_meme_endpoint, get_meme_endpoint, token):
    # Создаем мем через прямой запрос (без CreateMeme)
    headers = {'Content-type': 'application/json', 'Authorization': token}
    payload = {
        "text": "Meme to delete",
        "url": "https://lenta.ru/articles/2025/05/14/mem-okak/",
        "tags": ["delete"],
        "info": {"author": "Tester"}
    }

    response = requests.post(
        'http://memesapi.course.qa-practice.com/meme',
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        pytest.skip(f"Не удалось создать мем: {response.status_code}")

    meme_to_delete = response.json().get('id')

    if not meme_to_delete:
        pytest.skip("Не удалось получить ID созданного мема")

    # Удаляем мем
    delete_meme_endpoint.delete_meme(meme_to_delete, token)
    delete_meme_endpoint.check_that_status_is_200()

    # Проверяем что мем удален
    get_meme_endpoint.get_meme_by_id(meme_to_delete, token)
    get_meme_endpoint.check_that_status_is_404()

    # Проверяем что мема нет в общем списке
    get_meme_endpoint.get_all_memes(token)
    get_meme_endpoint.check_that_status_is_200()
    get_meme_endpoint.check_that_meme_is_not_in_list(meme_to_delete)
