from fastapi import APIRouter, Depends, status, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from backend.db_depends import get_db
from typing import Annotated
from models.Users import User
from schemas import UserCreate, UserUpdate

from main import *

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id=int):
    """
    Функция для возврата конкретного объекта user по id
    :param db:создает сессию подключения к базе данных
    :param user_id:int, Id
    :return:вовзращает объект из базы данных конкретно по id иначе выдает статус ошибки об его отсутствии
    """
    users = db.scalar(select(User).where(User.id == user_id))

    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    return db.scalars(select(User).where(User.id == user_id)).all()


@router.post("/registration")
async def registration_user(db: Annotated[Session, Depends(get_db)], registration_user: UserCreate):
    """
    Функция создания объекта Usera в базу данных
    :param db: создает сессию подключения к базе данных
    :param registration_user:объект создания Usera
    :return:Возвращает статус об успешном создании
    """
    db.execute(insert(User).values(username=registration_user.username,
                                   password=registration_user.password,
                                   age=registration_user.age))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Successful"
    }


@router.put('/user_update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UserUpdate):
    """
    Функция обновления объекта usera по его айди
    :param db: создает сессию подключения к базе данных
    :param user_id: int, id usera который будет обновляться
    :param update_user: объект обновления usera
    :return: возвращает статус о успешном или не успешном обновлении
    """
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no users found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        username=update_user.username,
        password=update_user.password,
        age=update_user.age
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }


@router.delete('/user_delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    """
    Функция удаления объекта usera по его айди
    :param db: создает сессию подключения к базе данных
    :param user_id: int: id usera который будет удаляться
    :return: возвращает статус о успешном или не успешном удалении
    """
    users_delete = db.scalar(select(User).where(User.id == user_id))
    if users_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }
