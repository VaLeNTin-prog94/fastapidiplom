from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Базовый класс для usera
    """
    id: int
    username: str
    password: str
    age: int


class UserCreate(UserBase):
    """Класс наследумый от UserBase дл редактирования объектов"""
    pass


class UserUpdate(UserBase):
    """Класс наследумый от UserBase дл обновления объектов"""
    pass


class Category(BaseModel):
    """
      Базовый класс для Категорий
      """
    id: int
    name: str


class CategoryUpdate(Category):
    """Класс наследумый от Category дл обновления объектов"""
    pass


class CreateCategory(Category):
    """Класс наследумый от Category дл редактирования объектов"""
    pass


class Bake(BaseModel):
    """
         Базовый класс для Выпечек
    """
    id: int
    title: str
    content: str
    is_published: bool
    cat_id: int


class CreateBake(Bake):
    """Класс наследумый от Bake дл редактирования объектов"""
    pass


class UpdateBake(Bake):
    """Класс наследумый от Bake дл обновления объектов"""
    pass
