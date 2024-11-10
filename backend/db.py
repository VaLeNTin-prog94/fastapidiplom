from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Подключение к базе данных
engine = create_engine("sqlite:///diplom.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """
    Для создания моделей необходима базовая модель, от которой потом наследуются остальные модели.
     Начиная с версии SQLAlchemy 2.0 для создания базовой модели надо создать класс, унаследованный от DeclarativeBase
    """
    pass
