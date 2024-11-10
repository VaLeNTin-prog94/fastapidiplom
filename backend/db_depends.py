from backend.db import SessionLocal


async def get_db():
    """
    Создание сессии для подключения к базе данных
    :return: открывает и закрывает после сессии
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
