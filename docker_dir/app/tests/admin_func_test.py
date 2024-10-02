from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from app.api.models import KittenModel, UpdateKittenModel
from tests.conftest import client, test_session_factory
from app.database.tables import ColorsTable, BreedsTable

# Заполним таблицы породы и цвета для тестирования функций

def test_create_colors():
    with test_session_factory() as session:
        session.add(ColorsTable(color='черный'))
        session.add(ColorsTable(color='желтый'))
        session.commit()

        query = select(ColorsTable.color)
        res = session.execute(query)
        colors = [color[0] for color in res.fetchall()]

        assert colors == ['черный', 'желтый']

def test_create_breeds():
    with test_session_factory() as session:
        session.add(BreedsTable(breed='крысоловка'))
        session.add(BreedsTable(breed='канадская'))
        session.commit()

        query = select(BreedsTable.breed)
        res = session.execute(query)
        breeds = [breed[0] for breed in res.fetchall()]

        assert breeds == ['крысоловка', 'канадская']

# Тестируем функции

def test_get_all_breeds():
    responce = client.get('/admin_func/breeds')
    
    assert responce.status_code == 200
    assert responce.json() == {'1': 'крысоловка',
                               '2' : 'канадская'}


def test_add_kitten():

    # Возьмем породу, которой нет

    kitten = KittenModel(id=0, name='string', color='черный', age=10, breed='string', description='string')

    responce =  client.post('/admin_func/kittens', json=jsonable_encoder(kitten))

    assert responce.status_code == 404
    assert responce.json() == {"detail": "Нет такой породы! Ознакомьтесь со списком пород"}

    # Возьмем цвет, которого нет

    kitten = KittenModel(id=0, name='string', color='string', age=10, breed='канадская', description='string')

    responce =  client.post('/admin_func/kittens', json=jsonable_encoder(kitten))

    assert responce.status_code == 404
    assert responce.json() == {'detail': 'Нет такого цвета! Введите цвет с маленькой буквы. Пример: черный, желтый'}
    
    # Корректный вызов

    kitten = KittenModel(id=0, name='string', color='черный', age=10, breed='канадская', description='string')
    
    responce =  client.post('/admin_func/kittens', json=jsonable_encoder(kitten))

    assert responce.status_code == 201
    assert responce.json() == {'Сообщение' : f'Информация о котенке string добавлена!'}

    kitten = KittenModel(id=1, name='string1', color='желтый', age=10, breed='канадская', description='string')
    
    responce =  client.post('/admin_func/kittens', json=jsonable_encoder(kitten))

    assert responce.status_code == 201
    assert responce.json() == {'Сообщение' : f'Информация о котенке string1 добавлена!'}

def test_get_all_kittens():
    responce =  client.get('/admin_func/kittens')

    assert responce.status_code == 200
    assert responce.json() == {'0' : 'string',
                               '1': 'string1'}



def test_get_kittens_filter_by_breed():

    # Такой породы нет
    responce = client.get('/admin_func/kittens_filter_by_breed?breed=string')

    assert responce.status_code == 404
    assert responce.json() == {'detail': 'Не найдено котят породы string! Ознакомьтесь со списком пород.'}

    #Есть
    responce = client.get('/admin_func/kittens_filter_by_breed?breed=канадская')

    assert responce.status_code == 200
    assert responce.json() == {'0' : 'string',
                               '1': 'string1'}

def test_get_info_about_kitten():
    
    # Нет такого котенка
    responce =  client.get('/admin_func/kittens/2')
    assert responce.status_code == 404
    assert responce.json() == {"detail": 'Такого котенка не существует!'}

    # Есть
    responce =  client.get('/admin_func/kittens/0')

    assert responce.status_code == 200
    assert responce.json() == {
                                "id": 0,
                                "name": "string",
                                "color": "черный",
                                "age": 10,
                                "breed": "канадская",
                                "description": "string"
                                }

def test_update_info_about_kitten():

    kitten = UpdateKittenModel(name='Васька')
    
    # Нет такого котенка
    responce =  client.put('/admin_func/kittens/2', json=jsonable_encoder(kitten))
    assert responce.status_code == 404
    assert responce.json() == {"detail": 'Такого котенка не существует!'}

    # Есть
    responce =  client.put('/admin_func/kittens/0', json=jsonable_encoder(kitten))
    assert responce.status_code == 200
    assert responce.json() == {'Сообщение' : 'Информация о котенке изменена!'}

def test_delete_kitten():
    
    responce =  client.delete('/admin_func/kittens/2')
    assert responce.status_code == 404
    assert responce.json() == {"detail": 'Такого котенка не существует!'}

    responce =  client.delete('/admin_func/kittens/0')
    assert responce.status_code == 200
    assert responce.json() == {'Сообщение' : 'Информация о котенке номер 0 удалена!'}

def test_add_breed():

    responce = client.post('/admin_func/breeds?breed=инопланетная')
    assert responce.status_code == 201
    assert responce.json() == {'Сообщение' : 'Информация о породе инопланетная добавлена!'}
    
def test_add_color():

    responce = client.post('/admin_func/colors?color=инопланетный')
    assert responce.status_code == 201
    assert responce.json() == {'Сообщение' : 'Информация о цвете инопланетный добавлена!'}

def test_get_all_colors():
    responce = client.get('/admin_func/colors')
    assert responce.status_code == 200
    assert responce.json() == {'1': 'черный',
                               '2' : 'желтый',
                               '3' : 'инопланетный'}
    
def test_delete_breed():

    responce = client.delete('/admin_func/breeds/3')
    assert responce.status_code == 200
    assert responce.json() == {'Сообщение' : 'Информация о породе номер 3 удалена!'}

def test_delete_color():

    responce = client.delete('/admin_func/colors/3')
    assert responce.status_code == 200
    assert responce.json() == {'Сообщение' : 'Информация о цвете номер 3 удалена!'}