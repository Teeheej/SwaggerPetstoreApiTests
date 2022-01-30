import json
from random import randint

import requests

import user_utils

base_url = 'https://petstore.swagger.io/v2/user'
user_data_for_creation = user_utils.get_test_users_data(number_of_entries=1)[0]


def test_login_with_no_credentials():
    response = requests.get(f'{base_url}/login')

    assert response.status_code == 400, f'got response code {response.status_code}, expected 400'


def test_login_with_invalid_credentials():
    query_params = {
        'username': f'definitelyInvalidUsername{randint(10000, 20000)}',
        'password': f'definitelyInvalidPassword{randint(10000, 20000)}',
    }
    response = requests.get(f'{base_url}/login', params=query_params)

    assert response.status_code == 400, f'got response code {response.status_code}, expected 400'


def test_create_user_with_dict_in_request_body():
    response = requests.post(
        base_url,
        data=user_data_for_creation,
        headers={'Content-Type': 'application/json'},
    )
    response_body = response.json()

    assert (
        response.status_code == response_body['code'] == 400
    ), f'got response code {response.status_code}, expected 400'
    assert response_body['message'] == 'bad input'


def test_create_user_with_empty_request_body():
    response = requests.post(base_url)
    response_body = response.json()

    assert (
        response.status_code == response_body['code'] == 400
    ), f'got response code {response.status_code}, expected 400'


def test_delete_user_with_no_username():
    response = requests.delete(f'{base_url}/')

    assert response.status_code == 400, f'got response code {response.status_code}, expected 400'


def test_edit_nonexistent_user():
    username = f'definitelyNonexistentUser{randint(100000, 200000)}'

    response = requests.put(
        f'{base_url}/{username}',
        data=json.dumps(user_data_for_creation),
        headers={'Content-Type': 'application/json', 'Cache-Control': 'no-cache'},
    )

    assert (
        response.status_code == 404
    ), f'attempt to edit nonexistent user {username} returned status code {response.status_code}'
