from fastapi import APIRouter, HTTPException, status, Depends

from app.api.models import KittenModel, UpdateKittenModel
from app.database.orm import (add_kitten_in_db, get_all_kittens_from_db, get_list_breeds_from_db, 
                              delete_kitten_from_db, get_info_about_kitten_from_db, change_info_about_kitten,
                              filter_by_breed, add_breed_in_db, add_color_in_db, delete_breed_from_db, 
                              delete_color_from_db, get_list_colors_from_db)

from app.database.engine import get_session

router = APIRouter(prefix='/admin_func', tags=['Функции по заданию'])

@router.get('/breeds', summary='Получение списка пород')
async def get_all_breeds(session = Depends(get_session)):
    res = get_list_breeds_from_db(session)
    return res

    
@router.get('/kittens', summary='Получение списка всех котят')
async def get_all_kittens(session = Depends(get_session)):
    res = get_all_kittens_from_db(session)
    return res


@router.get('/kittens_filter_by_breed', summary='Получение списка котят определенной породы')
async def get_kittens_filter_by_breed(breed: str, session = Depends(get_session)):
    if res := filter_by_breed(breed=breed, session=session):
        return res
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'Не найдено котят породы {breed}! Ознакомьтесь со списком пород.')


@router.get('/kittens/{id}', response_model=KittenModel, summary='Получение подробной информации о котенке')
async def get_info_about_kitten(id: int, session = Depends(get_session)):
    res = get_info_about_kitten_from_db(id=id, session=session)
    return res


@router.post('/kittens', summary='Добавление информации о котенке', status_code=201)
#async def add_kitten(credentials: Annotated[KittenModel, Form()]):
async def add_kitten(credentials: KittenModel, session = Depends(get_session)):
    add_kitten_in_db(credentials, session)
    return {'Сообщение' : f'Информация о котенке {credentials.name} добавлена!'}

@router.put('/kittens/{id}', summary='Изменение информации о котенке')
#async def update_info_about_kitten(id: int, credentials: Annotated[UpdateKittenModel, Depends()]):
async def update_info_about_kitten(id: int, credentials: UpdateKittenModel, session = Depends(get_session)):
    change_info_about_kitten(id, session, **credentials.model_dump())
    return {'Сообщение' : 'Информация о котенке изменена!'}


@router.delete('/kittens/{id}', summary='Удаление информации о котенке')
async def delete_kitten(id: int, session = Depends(get_session)):
    delete_kitten_from_db(id=id, session=session)
    return {'Сообщение' : f'Информация о котенке номер {id} удалена!'}

colors_and_breeds_router = APIRouter(prefix='/admin_func', tags=['Функции для полной работоспособности системы'])

@colors_and_breeds_router.post('/breeds', summary='Добавление информации о породе', status_code=201)
async def add_breed(breed: str, session = Depends(get_session)):
    add_breed_in_db(breed, session)
    return {'Сообщение' : f'Информация о породе {breed} добавлена!'}

@colors_and_breeds_router.post('/colors', summary='Добавление информации о цвете', status_code=201)
async def add_color(color: str, session = Depends(get_session)):
    add_color_in_db(color, session)
    return {'Сообщение' : f'Информация о цвете {color} добавлена!'}

@colors_and_breeds_router.delete('/breeds/{id}', summary='Удаление информации о породе')
async def delete_breed(id: int, session = Depends(get_session)):
    delete_breed_from_db(id=id, session=session)
    return {'Сообщение' : f'Информация о породе номер {id} удалена!'}

@colors_and_breeds_router.delete('/colors/{id}', summary='Удаление информации о цвете')
async def delete_color(id: int, session = Depends(get_session)):
    delete_color_from_db(id=id, session=session)
    return {'Сообщение' : f'Информация о цвете номер {id} удалена!'}

@colors_and_breeds_router.get('/colors', summary='Получение списка цветов')
async def get_all_colors(session = Depends(get_session)):
    res = get_list_colors_from_db(session)
    return res
