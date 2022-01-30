import json
from datetime import datetime
from time import sleep

import pytest
import requests
from dateutil import parser
from pytz import utc

import user_utils

base_url = 'https://petstore.swagger.io/v2/user'
user_data_for_creation = user_utils.get_test_users_data(number_of_entries=1)[0]
user_data_edited = user_utils.edit_user_data(user_data_for_creation)


# in case delete_user_test fails (for some reason this deletion works even if the test fails with 10 reruns)
@pytest.fixture(scope='module', autouse=True)
def cleanup_try_to_delete_users():
    yield
    for username in (user_data_for_creation['username'], user_data_edited['username']):
        response = requests.delete(f'{base_url}/{username}')
        if response.status_code == 200 and response.json()['message'] == username:
            print(f'User {username} was deleted during the after-tests cleanup')


@pytest.mark.dependency()
def test_create_user():
    response = requests.post(
        base_url,
        data=json.dumps(user_data_for_creation),
        headers={'Content-Type': 'application/json'},
    )
    response_body = response.json()
    assert response.status_code == 200
    assert int(response_body['message']) == user_data_for_creation['id'], 'unexpected user id in the response'


@pytest.mark.flaky(reruns=7)
@pytest.mark.dependency(depends=['test_create_user'])
def test_check_user_data(user_data=user_data_for_creation, is_deleted=False):
    sleep(3)  # give the server some time to process user creation/editing before the check
    response = requests.get(
        f'{base_url}/{user_data["username"]}',
        headers={
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
    )
    response_body = response.json()

    if is_deleted:
        assert response.status_code == 404, f'response code is {response.status_code}; expected 404'
        assert response_body['code'] == 1, 'unexpected "code" attribute value in the response body'
        assert response_body['message'] == 'User not found', 'unexpected message in the response body'
    else:
        assert response.status_code == 200, f'response code is {response.status_code}; expected 200'
        assert response_body == user_data, 'user data values are not as expected'


@pytest.mark.dependency(depends=['test_create_user'])
def test_login():
    query_params = {
        'username': user_data_for_creation['username'],
        'password': user_data_for_creation['password'],
    }
    response = requests.get(f'{base_url}/login', params=query_params)

    x_expires_after = response.headers['X-Expires-After']
    x_rate_limit = response.headers['X-Rate-Limit']
    now = datetime.utcnow().replace(tzinfo=utc)

    assert int(response.status_code) == 200
    assert 'logged in user session:' in response.json()['message'], 'no expected substring in the message attribute'
    assert now <= parser.parse(x_expires_after), 'token expire time should not be earlier than current time'
    assert int(x_rate_limit) == 5000, 'unexpected value of request rate limit'


@pytest.mark.dependency(depends=['test_login'])
def test_logout():
    response = requests.get(f'{base_url}/logout')

    assert response.status_code == 200
    assert response.json()['message'] == 'ok', 'unexpected "message" attribute value'


@pytest.mark.flaky(reruns=7)
@pytest.mark.dependency(depends=['test_create_user'])
def test_update_user_data():
    response = requests.put(
        f'{base_url}/{user_data_for_creation["username"]}',
        data=json.dumps(user_data_edited),
        headers={
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
    )

    assert response.status_code == 200, f'response code is {response.status_code}; expected 200'
    if response.status_code == 200:
        test_check_user_data(user_data=user_data_edited)


@pytest.mark.flaky(reruns=5)
@pytest.mark.dependency(depends=['test_update_user_data'])
def test_delete_user():

    username = user_data_edited['username']
    response = requests.delete(
        f'{base_url}/{username}',
        headers={'Content-Type': 'application/json', 'Cache-Control': 'no-cache'},
    )

    assert response.status_code == 200, f'response code is {response.status_code}; expected 200'
    if response.status_code == 200:  # if response is 404, the body is plain text that causes json() func to crash
        assert response.json()['message'] == username, 'unexpected username in the response body'
        test_check_user_data(user_data=user_data_edited, is_deleted=True)
