import allure


@allure.story('Negative tests')
def test_get_memes_without_token(negative_endpoint):
    negative_endpoint.get_all_memes_without_token_401()


@allure.story('Negative tests')
def test_create_meme_without_token(negative_endpoint):
    payload = {
        "text": "Test Meme",
        "url": "http://memesapi.course.qa-practice.com",
        "tags": ["test"],
        "info": {"author": "Test"}
    }
    negative_endpoint.create_meme_without_token_401(payload)


@allure.story('Negative tests')
def test_get_meme_by_id_without_token(negative_endpoint, meme_id):
    negative_endpoint.get_meme_by_id_without_token_401(meme_id)


@allure.story('Negative tests')
def test_update_meme_without_token(negative_endpoint, meme_id):
    payload = {
        "id": meme_id,
        "text": "Updated Meme",
        "url": "http://memesapi.course.qa-practice.com",
        "tags": ["test"],
        "info": {"author": "Test"}
    }
    negative_endpoint.update_meme_without_token_401(meme_id, payload)


@allure.story('Negative tests')
def test_delete_meme_without_token(negative_endpoint, meme_id):
    negative_endpoint.delete_meme_without_token_401(meme_id)


@allure.story('Negative tests')
def test_authorize_empty_name(negative_endpoint):
    negative_endpoint.authorize_empty_name_400()


@allure.story('Negative tests')
def test_authorize_without_name(negative_endpoint):
    negative_endpoint.authorize_without_name_400()


@allure.story('Negative tests')
def test_create_meme_empty_text(negative_endpoint, token):
    negative_endpoint.create_meme_empty_text_400(token)


@allure.story('Negative tests')
def test_create_meme_invalid_url(negative_endpoint, token):
    negative_endpoint.create_meme_invalid_url_400(token)


@allure.story('Negative tests')
def test_create_meme_without_text(negative_endpoint, token):
    negative_endpoint.create_meme_without_text_400(token)


@allure.story('Negative tests')
def test_create_meme_without_url(negative_endpoint, token):
    negative_endpoint.create_meme_without_url_400(token)


@allure.story('Negative tests')
def test_update_meme_empty_text(negative_endpoint, token, meme_id):
    negative_endpoint.update_meme_empty_text_400(token, meme_id)


@allure.story('Negative tests')
def test_update_meme_invalid_url(negative_endpoint, token, meme_id):
    negative_endpoint.update_meme_invalid_url_400(token, meme_id)


@allure.story('Negative tests')
def test_get_nonexistent_meme(negative_endpoint, token):
    negative_endpoint.get_nonexistent_meme_404(token)


@allure.story('Negative tests')
def test_update_nonexistent_meme(negative_endpoint, token):
    negative_endpoint.update_nonexistent_meme_404(token)


@allure.story('Negative tests')
def test_delete_nonexistent_meme(negative_endpoint, token):
    negative_endpoint.delete_nonexistent_meme_404(token)


@allure.story('Negative tests')
def test_use_patch_method(negative_endpoint, token, meme_id):
    negative_endpoint.use_patch_method_405(meme_id, token)


# Для теста двойного удаления используем существующие эндпоинты
@allure.story('Negative tests')
def test_delete_already_deleted_meme(create_meme_endpoint, delete_meme_endpoint, token):
    # Создаем мем
    payload = {
        "text": "Meme to delete twice",
        "url": "http://memesapi.course.qa-practice.com",
        "tags": ["delete"],
        "info": {"author": "Tester"}
    }
    create_meme_endpoint.create_new_meme(payload, token)
    meme_to_delete = create_meme_endpoint.json['id']

    # Удаляем первый раз
    delete_meme_endpoint.delete_meme(meme_to_delete, token)
    delete_meme_endpoint.check_that_status_is_200()

    # Пытаемся удалить второй раз
    delete_meme_endpoint.delete_meme(meme_to_delete, token)
    delete_meme_endpoint.check_that_status_is_404()
