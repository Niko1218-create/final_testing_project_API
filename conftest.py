import pytest
from endpoints.authorize import Authorize
from endpoints.get_meme import GetMeme
from endpoints.create_meme import CreateMeme
from endpoints.put_meme import UpdateMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.negative_endpoint import NegativeEndpoint


@pytest.fixture()
def authorize_endpoint():
    return Authorize()


@pytest.fixture()
def get_meme_endpoint():
    return GetMeme()


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def negative_endpoint():
    return NegativeEndpoint()


@pytest.fixture(scope="session")
def token():
    auth = Authorize()
    auth.create_token()
    return auth.token


@pytest.fixture()
def invalid_token():
    return 'invalid_token_12345'


@pytest.fixture()
def meme_id(create_meme_endpoint, token):
    payload = {
        "text": "Test Meme",
        "url": "https://example.com/test.jpg",
        "tags": ["test", "funny"],
        "info": {"author": "Tester"}
    }

    create_meme_endpoint.create_new_meme(payload, token)
    test_meme_id = create_meme_endpoint.meme_id

    yield test_meme_id

    delete_endpoint = DeleteMeme()
    delete_endpoint.delete_meme(test_meme_id, token)
