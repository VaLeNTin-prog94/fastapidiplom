from backend.db import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    '''
     Создание таблиц Users  в базе данных
     Наследуется от базового класса
     '''
    __tablename__ = "users"
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    age = Column(Integer)
