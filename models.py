from sqlalchemy import Column, Integer, MetaData, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

from settings import PostgresConfiguration
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

pg = PostgresConfiguration()
engine = create_engine(pg.postgres_db_path)
meta = MetaData(engine)
Base = declarative_base()


class LocationTable(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid', ondelete='CASCADE'))
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String)
    postcode = Column(Integer)
    state = Column(String)
    street_name = Column(String)
    street_number = Column(Integer)
    timezone_description = Column(String)
    timezone_offset = Column(String)


class LoginTable(Base):
    __tablename__ = 'logins'
    login_id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid', ondelete='CASCADE'))
    md5 = Column(String)
    password = Column(String)
    salt = Column(String)
    sha1 = Column(String)
    sha256 = Column(String)
    username = Column(String)


class UserTable(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cell = Column(String)
    dob_date = Column(DateTime)
    email = Column(String)
    gender_m = Column(Boolean)
    id_name = Column(String)
    id_value = Column(String)

    location = relationship(LocationTable, backref="users", passive_deletes=True)
    login = relationship(LoginTable, backref="users", passive_deletes=True)
    name_first = Column(String)
    name_last = Column(String)
    name_title = Column(String)
    nat = Column(String)
    phone = Column(String)
    picture_id = Column(Integer)
    registered_date = Column(DateTime)


def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)


if __name__ == '__main__':
    # create_tables()
    Base.metadata.drop_all(engine)
