from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.Categorys import Category
from schemas import CreateCategory,CategoryUpdate
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/category', tags=['category'])

@router.get('/all_category')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    """
    Функция возврата всех категорий из базы данных
    :param db: создает сессию подключения к базе данных
    :return: возвращает объект содержащий в себе информацию о категориях из базы данных
    """
    category = db.scalars(select(Category).where()).all()
    return category

@router.get('/category_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], category_id=int):
    """
    Функция для воpdрата конкретного объекта категории по id
    :param db: создает сессию подключения к базе данных
    :param category_id: int, Id
    :return: вовзращает объект из базы данных конкртно по id иначе выдает статус ошибки об его отсуствии
    """
    category = db.scalar(select(Category).where(Category.id == category_id))

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    return db.scalars(select(Category).where(Category.id == category_id)).all()


@router.post("/category_add")
async def registration_category(db:Annotated[Session,Depends(get_db)],registration_category:CreateCategory):
    """
     Функция создания объекта категорий в базу данных
    :param db: создает сессию подключения к базе данных
    :param registration_category: объект создания категорий
    :return: возвращает статус создания объекта
    """
    db.execute(insert(Category).values(name=registration_category.name))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Successful"
    }

@router.put('/update_category')
async def update_category(db: Annotated[Session, Depends(get_db)], category_id: int, update_category:CategoryUpdate ):
    """
    Функция обновления объекта категорий по его айди
    :param db: создает сессию подключения к базе данных
    :param category_id: int, id категории который будет обновляться
    :param update_category: объект обновления категорий
    :return: возвращает статус о успешном или не успешном обновлении
    """
    category = db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(update(Category).where(Category.id == category_id).values(
        name=update_category.name
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }
@router.delete('/delete_category')
async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):
    """
    Функция удаления объекта категории по его айди
    :param db: создает сессию подключения к базе данных
    :param category_id: int: id категории который будет удаляться
    :return: озвращает статус о успешном или не успешном удалении
    """
    category_delete = db.scalar(select(Category).where(Category.id == category_id))
    if category_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(delete(Category).where(Category.id == category_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }