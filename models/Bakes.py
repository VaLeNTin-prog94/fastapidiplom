from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class Bake(Base):
    '''
    Создание таблиц Bake  в базе данных
    Наследуется от базового класса
    '''
    __tablename__ = "bakes"
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    is_published = Column(Boolean)
    cat_id = Column(Integer, ForeignKey("category.id"))
