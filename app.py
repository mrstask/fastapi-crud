import uvicorn
from fastapi import FastAPI

from handlers import add_user_to_db, get_users_from_api, get_user_by_uuid, get_users_from_db, delete_user_from_db
from models import create_tables
from settings import APP_PORT

app = FastAPI()


@app.post('/users/', summary='populate users', tags=['Users'])
async def populate_users(quantity: int, male: bool):
    users = get_users_from_api(quantity, 'male' if male else 'female')
    user_ids = []
    for user in users['results']:
        user_ids.append(add_user_to_db(user))
    return dict(added_user_ids=user_ids)


@app.get('/users/', summary='get all users', tags=['Users'])
async def get_users():
    users_data = get_users_from_db()
    if not users_data:
        users_data = 'No users in database'
    return dict(users_data=users_data)


@app.get('/users/{user_uuid}', summary='get user by user_uuid', tags=['Users'])
async def get_user(user_uuid: str):
    user_data = get_user_by_uuid(user_uuid)
    if not user_data:
        user_data = 'Could not find user in database'
    return dict(user_data=user_data)


@app.delete('/users/{user_uuid}', summary='delete user by user_uuid', tags=['Users'])
async def delete_user(user_uuid: str):
    result = delete_user_from_db(user_uuid)
    if result:
        return dict(message=f'User {user_uuid} deleted successfully')
    return dict(message=f'User not presented in database')


if __name__ == '__main__':
    create_tables()
    uvicorn.run(app, host='0.0.0.0', port=int(APP_PORT))
