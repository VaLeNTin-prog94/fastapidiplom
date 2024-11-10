from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.Bakes import Bake
from models.Categorys import Category
from schemas import CreateBake, UpdateBake
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/bake', tags=['bake'])


@router.get('/all_bake')
async def all_bake(db: Annotated[Session, Depends(get_db)]):
    '''
    Функция возврата всех видов выпечки из базы данных
    :param db:создает сессию подключения к базе данных
    :return: возвращает объект содержащий в себе информацию о всех выпечках из базы данных
    '''
    bake = db.scalars(select(Bake).where()).all()
    return bake


@router.get('/bake_id')
async def bake_by_id(db: Annotated[Session, Depends(get_db)], bake_id=int):
    """
    Функция для возврата конкретного объекта выпечек по id
    :param db: создает сессию подключения к базе данных
    :param bake_id: int, Id
    :return:вовзращает объект из базы данных конкретно по id иначе выдает статус ошибки об его отсутствии
    """
    bake = db.scalar(select(Bake).where(Bake.id == bake_id))

    if bake is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bake was not found'
        )
    return db.scalars(select(Bake).where(Bake.id == bake_id)).all()


@router.post('/bake_create')
async def create_bake(db: Annotated[Session, Depends(get_db)], cat_id: int, create_task: CreateBake):
    """
    Функция создания объекта выпечки в базу данных
    :param db: создает сессию подключения к базе данных
    :param cat_id: int, id категории с которым связана данный тип выпечки
    :param create_task: объект создания выпечек
    :return: возвращает статус создания объекта успешно или не успешно если у объекта не существует категории
    """
    category = db.scalar(select(Category).where(Category.id == cat_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bake was not found'
        )
    db.execute(insert(Bake).values(title=create_task.title,
                                   content=create_task.content,
                                   is_published=create_task.is_published,
                                   cat_id=cat_id,
                                   ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': "Successful"
    }


@router.put('/bake_update')
async def update_bake(db: Annotated[Session, Depends(get_db)], bake_id: int, update_bake: UpdateBake):
    """
    Функция обновления объекта выпечки по его айди
    :param db:создает сессию подключения к базе данных
    :param bake_id:int, id выпечки который будет обновляться
    :param update_bake: объект обновления выпечек
    :return: возвращает статус о успешном или не успешном обновлении
    """
    bake = db.scalar(select(Bake).where(Bake.id == bake_id))
    if bake is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bake is no bake found'
        )
    db.execute(update(Bake).where(Bake.id == bake_id).values(
        title=update_bake.title,
        content=update_bake.content,
        is_published=update_bake.is_published,
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Bake update is successful'
    }


@router.delete('/bake_delete')
async def delete_bake(db: Annotated[Session, Depends(get_db)], bake_id: int):
    """
    Функция удаления объекта выпечки по его айди
    :param db: создает сессию подключения к базе данных
    :param bake_id: int: id выпечки который будет удаляться
    :return: возвращает статус о успешном или не успешном удалении
    """
    task_delete = db.scalar(select(Bake).where(Bake.id == bake_id))
    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bake is no category found'
        )
    db.execute(delete(Bake).where(Bake.id == bake_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Bake delete is successful'
    }
