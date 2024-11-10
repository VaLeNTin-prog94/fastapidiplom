from backend.db import Base
from sqlalchemy import Column, Integer, String


class Category(Base):
    '''
     Создание таблиц Category  в базе данных
     Наследуется от базового класса
     '''
    __tablename__ = "category"
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    def __str__(self):
        '''
        Специальный метод, предназначенный для представления строкового представления объекта
        :return: Возвращает удобочитаемое (или неформальное) стровое представление объекта
        '''
        return self.name