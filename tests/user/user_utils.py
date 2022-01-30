from csv import DictReader
from random import sample as random_sample
from random import randint

from tests.definitions import USER_DATA_CSV_PATH


def get_test_users_data(number_of_entries: int) -> list:
    with open(USER_DATA_CSV_PATH) as user_data:

        all_users = [line for line in DictReader(user_data)]
        users_list = random_sample(all_users, number_of_entries)

        # change attribute value types to match endpoint response body
        for user_entry in users_list:
            for attribute in ('id', 'userStatus'):
                user_entry[attribute] = int(user_entry[attribute])
            # additional randomization to increase amount of unique users
            user_entry['username'] += str(randint(1000, 9999))

        return users_list


def edit_user_data(user_data: dict) -> dict:
    edited_user = get_test_users_data(1)[0]
    edited_user['id'] = user_data['id']
    return edited_user
