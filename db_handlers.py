from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import PostgresConfiguration
from models import UserTable, LocationTable, LoginTable
from sqlalchemy.exc import InvalidRequestError


class PosgresHandler:
    def __init__(self, db_string):
        self.engine = create_engine(db_string)
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    # --------------------------------------------------USERS----------------------------------------------------
    def add_user(self, data: dict):
        user = self.get_user_by_uuid(data['uuid'])
        if user:
            return user
        user = UserTable(**data)
        self.session.add(user)
        try:
            self.session.commit()
        except InvalidRequestError:
            self.session.rollback()
            raise InvalidRequestError
        return user

    def get_users(self):
        users = self.session.query(UserTable, LoginTable, LocationTable).join(LoginTable).join(LocationTable).all()
        if users:
            return users

    def get_user_by_uuid(self, uuid: str):
        user = self.session.query(UserTable, LoginTable, LocationTable).join(LoginTable).join(LocationTable).filter(
            UserTable.uuid == uuid).all()
        if user:
            return user

    def delete_user(self, uuid: int):
        self.session.query(UserTable).filter(UserTable.uuid == uuid).delete()
        try:
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            raise InvalidRequestError

    # --------------------------------------------------LOCATIONS----------------------------------------------------
    def add_location(self, data: dict):
        location_table = LocationTable(**data)
        self.session.add(location_table)
        try:
            self.session.commit()
        except InvalidRequestError:
            self.session.rollback()
            raise InvalidRequestError
        return location_table

    def get_location_by_id(self, location_id: int):
        location = self.session.query(LocationTable).filter_by(location_id=location_id).scalar()
        if location:
            return location

    # --------------------------------------------------LOGIN----------------------------------------------------
    def add_login(self, data: dict):
        login_table = LoginTable(**data)
        self.session.add(login_table)
        try:
            self.session.commit()
        except InvalidRequestError:
            self.session.rollback()
            raise InvalidRequestError
        return login_table

    def get_login_by_id(self, login_id: int):
        login = self.session.query(LoginTable).filter_by(login_id=login_id).scalar()
        if login:
            return login


pg_handler = PosgresHandler(PostgresConfiguration().postgres_db_path)
