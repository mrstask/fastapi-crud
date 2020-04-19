import requests
from db_handlers import pg_handler
from datetime import datetime


def get_users_from_api(results: int, gender: str):
    response = requests.get(f'https://randomuser.me/api?results={results}&gender={gender}')
    if response.status_code == 200:
        return response.json()


def add_user_to_db(user_data: dict):
    user = pg_handler.add_user(dict(uuid=user_data['login']['uuid'],
                                    cell=user_data['cell'],
                                    dob_date=user_data['dob']['date'],
                                    email=user_data['email'],
                                    gender_m=True if user_data['gender'] == 'male' else False,
                                    id_name=user_data['id']['name'],
                                    id_value=user_data['id']['value'],
                                    name_first=user_data['name']['first'],
                                    name_last=user_data['name']['last'],
                                    name_title=user_data['name']['title'],
                                    nat=user_data['nat'],
                                    phone=user_data['phone'],
                                    picture_id=user_data['picture']['large'].split('/')[-1].replace('.jpg', ''),
                                    registered_date=user_data['registered']['date']
                                    ))
    pg_handler.add_login(dict(md5=user_data['login']['md5'],
                              user_uuid=user_data['login']['uuid'],
                              password=user_data['login']['password'],
                              salt=user_data['login']['salt'],
                              sha1=user_data['login']['sha1'],
                              sha256=user_data['login']['sha256'],
                              username=user_data['login']['username'])
                         )
    pg_handler.add_location(dict(city=user_data['location']['city'],
                                 user_uuid=user_data['login']['uuid'],
                                 latitude=user_data['location']['coordinates']['latitude'],
                                 longitude=user_data['location']['coordinates']['longitude'],
                                 country=user_data['location']['country'],
                                 state=user_data['location']['state'],
                                 street_name=user_data['location']['street']['name'],
                                 street_number=user_data['location']['street']['number'],
                                 timezone_description=user_data['location']['timezone']['description'],
                                 timezone_offset=user_data['location']['timezone']['offset']
                                 ))
    return user.uuid


def get_users_from_db():
    normalized_users = list()
    users = pg_handler.get_users()

    for user in users:
        normalized_users.append(normalize_result(user))

    return users


def get_user_by_uuid(uuid: str):
    user_data = pg_handler.get_user_by_uuid(uuid)
    if user_data:
        return normalize_result(user_data[0])


def delete_user_from_db(user_uuid):
    return pg_handler.delete_user(user_uuid)


def normalize_result(user_data):
    return {'cell': user_data.UserTable.cell,
            'dob': {'age': round((datetime.now() - user_data.UserTable.dob_date).days / 365),
                    'date': user_data.UserTable.dob_date},
            'email': user_data.UserTable.email,
            'gender': 'male' if user_data.UserTable.gender_m else 'female',
            'id': {'name': user_data.UserTable.id_name, 'value': user_data.UserTable.id_value},
            'location': {'city': user_data.LocationTable.city,
                         'coordinates': {'latitude': user_data.LocationTable.latitude,
                                         'longitude': user_data.LocationTable.longitude},
                         'country': user_data.LocationTable.country,
                         'postcode': user_data.LocationTable.postcode,
                         'state': user_data.LocationTable.state,
                         'street': {'name': user_data.LocationTable.street_name,
                                    'number': user_data.LocationTable.street_number},
                         'timezone': {'description': user_data.LocationTable.timezone_description,
                                      'offset': user_data.LocationTable.timezone_offset}},
            'login': {'md5': user_data.LoginTable.md5,
                      'password': user_data.LoginTable.password,
                      'salt': user_data.LoginTable.salt,
                      'sha1': user_data.LoginTable.sha1,
                      'sha256': user_data.LoginTable.sha256,
                      'username': user_data.LoginTable.username,
                      'uuid': user_data.UserTable.uuid},
            'name': {'first': user_data.UserTable.name_first,
                     'last': user_data.UserTable.name_last,
                     'title': user_data.UserTable.name_title},
            'nat': user_data.UserTable.nat,
            'phone': user_data.UserTable.phone,
            'picture': {'large': f'https://randomuser.me/api/portraits/women/{user_data.UserTable.picture_id}.jpg',
                        'medium': f'https://randomuser.me/api/portraits/med/women/{user_data.UserTable.picture_id}.jpg',
                        'thumbnail': f'https://randomuser.me/api/portraits/thumb/women/{user_data.UserTable.picture_id}.jpg'},
            'registered': {'age': round((datetime.now() - user_data.UserTable.registered_date).days / 365),
                           'date': {user_data.UserTable.registered_date}}}
