from fastapi import FastAPI, APIRouter, Depends, status, HTTPException, Request, Form
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from backend import db
from backend.db_depends import get_db
from models.Bakes import Bake
from models.Categorys import Category
from routers import user, category, bake
from typing import Annotated
from models.Users import User
from schemas import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete

app = FastAPI()

# группируем маршрутры нашего веб приложения
app.include_router(user.router)
app.include_router(category.router)
app.include_router(bake.router)

# подключаем шаблоны страниц
templates = Jinja2Templates(directory="templates")
# список для хранеия главного меню и их url
menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Регистрация", 'url_name': 'registration'},
    {'title': "Войти", 'url_name': 'login'},
]
# подлючаем статистические файлы  в котором хранятся css
app.mount("/static", StaticFiles(directory="static"), name='static')


@app.get('/')
def welcome(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Функция главной страницы
    :param request:запрос
    :param db: создает сессию подключения к базе данных
    :return:возвращает страницу main
    """
    bake = db.scalars(select(Bake).where()).all()
    return templates.TemplateResponse("main.html", context={"request": request,
                                                            "menu": menu,
                                                            'category': db.scalars(select(Category).where()).all(),
                                                            "bake": bake})


@app.get('/about')
def abouts(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Функция для обработки страницы об информации
    :param request: запрос
    :param db: создает сессию подключения к базе данных
    :return: возвращает страницу about
    """

    return templates.TemplateResponse("about.html", context={"request": request,
                                                             "menu": menu,
                                                             'category': db.scalars(select(Category).where()).all()})


@app.get('/contact')
def contacts(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Функция для обработки страницы контакты
    :param request: запрос
    :param db: создает сессию подключения к базе данных
    :return: возвращает страницу contact
    """
    return templates.TemplateResponse("contact.html", context={"request": request,
                                                               "menu": menu,
                                                               'category': db.scalars(select(Category).where()).all()})


@app.get('/add_page')
def add_page(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Функция для обработки страницы добавления выпечек
    :param request: запрос
    :param db: создает сессию подключения к базе данных
    :return: возвращает страницу add_page
    """
    return templates.TemplateResponse("add_page.html", context={"request": request,
                                                                "menu": menu,
                                                                'category': db.scalars(select(Category).where()).all()})


@app.get('/login')
def login(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Функция для входа пользователя в систему
    :param request:запрос
    :param db:создает сессию подключения к базе данных
    :return: возвращает страницу login
    """
    return templates.TemplateResponse("login.html", context={"request": request,
                                                             "menu": menu,
                                                             'category': db.scalars(select(Category).where()).all()})


@app.get('/registration')
def registration(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Функция для регистрации пользователей
    :param request:запрос
    :param db:создает сессию подключения к базе данных
    :return: возвращает страницу registration
    """
    return templates.TemplateResponse("registration.html",
                                      context={"request": request,
                                               "menu": menu,
                                               'category': db.scalars(select(Category).where()).all()})
