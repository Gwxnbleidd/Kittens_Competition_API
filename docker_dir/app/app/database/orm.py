from sqlalchemy import select, delete, update
from fastapi import HTTPException, status

from app.database.engine import engine,Base, session_factory
from app.database.tables import KittensTable, ColorsTable, BreedsTable
from app.api.models import KittenModel

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    fill_colors()
    fill_breeds()
    fill_kittens()

def check_exist_db():
    with session_factory() as session:
        res = session.execute(select(ColorsTable.color).limit(1))
        return res.fetchone()

def add_kitten_in_db(credentials: KittenModel, session):
    color = session.execute(select(ColorsTable.id).filter_by(color=credentials.color)).fetchone()
    if not color:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='Нет такого цвета! Введите цвет с маленькой буквы. Пример: черный, желтый')
        
    breed = session.execute(select(BreedsTable.id).filter_by(breed=credentials.breed)).fetchone()
    if not breed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='Нет такой породы! Ознакомьтесь со списком пород')
        
    session.add(KittensTable(id= credentials.id, name=credentials.name, color_id=color[0],age=credentials.age,
                                breed_id=breed[0], description=credentials.description))
    session.commit()
    
def get_all_kittens_from_db(session) -> dict[str, str]:
    query = select(KittensTable.id, KittensTable.name).select_from(KittensTable)
    res = session.execute(query)
    kittens = {kitten[0]: kitten[1] for kitten in res.fetchall()}
    return kittens

def get_list_breeds_from_db(session) -> dict[str,str]:
    query = select(BreedsTable.id, BreedsTable.breed).select_from(BreedsTable)
    res = session.execute(query)
    breeds = {breed[0]:breed[1] for breed in res.fetchall()}
    return breeds
    
def filter_by_breed(breed: str, session) -> dict[str, str]:
    query = (select(KittensTable.id, KittensTable.name)
            .select_from(KittensTable)
            .join(BreedsTable, KittensTable.breed_id == BreedsTable.id)
            .filter(BreedsTable.breed==breed))
    res = session.execute(query)
    kittens = {kitten[0]: kitten[1] for kitten in res.fetchall()}
    return kittens
    
def get_info_about_kitten_from_db(id: int, session):
    query = (select(KittensTable.id, KittensTable.name, KittensTable.age, 
                    ColorsTable.color, BreedsTable.breed, KittensTable.description)
            .select_from(KittensTable)
            .join(BreedsTable, KittensTable.breed_id == BreedsTable.id)
             .join(ColorsTable, KittensTable.color_id == ColorsTable.id)
             .filter(KittensTable.id==id))
    res = session.execute(query).fetchone()
    if res is not None:
        return res
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого котенка не существует!')

def change_info_about_kitten(id,session, **kwargs):
    #Проверяем есть ли такой котенок
    if session.get(KittensTable, id):
        for key, val in kwargs.items():
            if val is not None:
                if key == 'name':
                    session.execute(update(KittensTable).filter_by(id=id).values(name=val))
                elif key == 'color':
                    # Проверяем есть ли такой цвет
                    if session.execute(select(ColorsTable.color).filter_by(color=val)):
                        session.execute(update(KittensTable).filter_by(id=id).values(color=val))
                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='Нет такого цвета!\n Введите цвет с маленькой буквы, например "черный" или "желтый"')
                elif key == 'age':
                    session.execute(update(KittensTable).filter_by(id=id).values(age=val))
                elif key == 'breed':
                    if session.execute(select(BreedsTable.breed).filter_by(breed=val)):
                        session.execute(update(KittensTable).filter_by(id=id).values(breed=val))
                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='Нет такой породы!\n Ознакомьтесь со списком пород')
                elif key == 'description':
                    session.execute(update(KittensTable).filter_by(id=id).values(description=val))
        session.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого котенка не существует!')
    
def delete_kitten_from_db(id: int, session):
    #Проверяем есть ли такой котенок
    if session.get(KittensTable, id):
        query = delete(KittensTable).filter_by(id=id)
        session.execute(query)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого котенка не существует!')
    
def fill_colors():
    with session_factory() as session:
        colors = [
        "белый", "черный", "серый", "красный", "оранжевый", "желтый", 
        "зеленый", "голубой", "синий", "фиолетовый", "розовый", "рыжий",
        "коричневый", "бежевый", "золотой", "серебристый",
        "бордовый", "пурпурный", "лазурный", "бирюзовый", 
        "лиловый", "песочный", "малиновый", "фуксия", 
        "оливковый", "терракотовый", "индиго", "хаки", 
        "персиковый", "лавандовый", "небесный", "изумрудный", 
        "коралловый", "абрикосовый", "мятный", "сиреневый",
        "синий сапфир", "вишневый", "шоколадный", "топазовый", 
        "марсала", "бирюзовый", "темно-синий", "светло-зеленый",
        "желто-коричневый", "темно-красный", "светло-коричневый", 
        "темно-фиолетовый", "темно-зеленый", "светло-голубой", 
        "темно-желтый", "светло-розовый", "темно-оранжевый", "лысый"
        "темно-серый", "светло-серый", "темно-синий", "светло-синий","трехшерстный"
        ]
        for color in colors:
            session.add(ColorsTable(color=color))
        session.commit()

def fill_breeds():
    with session_factory() as session:
        breeds = [
        "абиссинская", "американская короткошерстная", "американская длинношерстная",
        "ангорская", "бенгальская", "бирманская", "британская короткошерстная",
        "бурманская", "сиамская", "шотландская вислоухая", "персидская", 
        "русская голубая", "сфинкс", "мейн-кун", "корниш-рекс", 
        "девон-рекс", "сибирская", "немецкая короткошерстная", "японский бобтейл", 
        "американский керл", "манчкин", "хималайская",  "экзотическая",
        "британская длинношерстная", "бурмилла", "балинезийская", "тайская",
        "австралийская", "шотландская прямоухая", "американский бобтейл", 
         "ашера", "чаузи", "саванна", "ориентальная", "рагамаффин", 
         "балтийская", "бомбейская", "турецкая ангора", "цыганская", 
        "норвежская лесная", "канадская"
        ]
        for breed in breeds:
            session.add(BreedsTable(breed=breed))
        session.commit()

def fill_kittens():
    with session_factory() as session:
        add_kitten_in_db(KittenModel(name='Мягколапка', color='черный', age=3, 
                                    breed='бирманская', description='Прекрасный котенок из мультика "Кот в сапогах"'), session)
        add_kitten_in_db(KittenModel(name='Кот в сапогах', color='рыжий', age=5, 
                                    breed='бирманская', description='Прекрасный котик из мультика "Кот в сапогах"'), session)
        add_kitten_in_db(KittenModel(name='Пушистик', color='белый', age=5, 
                                    breed='мейн-кун', description='Большой и серьезный котенок'), session)
        add_kitten_in_db(KittenModel(name='Леопольд', color='серый', age=4, 
                                    breed='сфинкс', description='Миролюбивый котенок'), session)


def add_breed_in_db(breed: str, session):
    session.add(BreedsTable(breed=breed))
    session.commit()

def add_color_in_db(color: str, session):
    session.add(ColorsTable(color=color))
    session.commit()

def delete_breed_from_db(id: int, session):
    #Проверяем есть ли такой котенок
    if session.get(BreedsTable, id):
        query = delete(BreedsTable).filter_by(id=id)
        session.execute(query)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такой породы не существует!')
    
def delete_color_from_db(id: int, session):
    #Проверяем есть ли такой котенок
    if session.get(ColorsTable, id):
        query = delete(ColorsTable).filter_by(id=id)
        session.execute(query)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого цвета не существует!')
    
def get_list_colors_from_db(session) -> dict[str,str]:
    query = select(ColorsTable.id, ColorsTable.color)
    res = session.execute(query)
    colors = {color[0]:color[1] for color in res.fetchall()}
    return colors
    