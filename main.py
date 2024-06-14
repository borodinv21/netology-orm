import os
import sqlalchemy
import json

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Stock, Shop, Sale, Book

load_dotenv()

USERNAME = os.getenv('db_USERNAME')
PASSWORD = os.getenv('db_PASSWORD')
DB_NAME = os.getenv('db_NAME')


if __name__ == '__main__':
    DSN = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{DB_NAME}"

    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))

    session.commit()

    publisher_info = input('Введите Имя или ID автора: ')

    sales = session.query(Book.title, Shop.name, Sale.price,  Sale.date_sale, Stock, Sale, Publisher).join(Shop).join(Book).join(Sale).join(Publisher).where(Publisher.id == publisher_info if publisher_info.isdigit() else Publisher.name == publisher_info).all()

    if sales:
        for sale in sales:
            print(f'{sale[0]} | {sale[1]} | {sale[2]} | {sale[3]}')
    else:
        print('Такого автора не существует...')

    session.close()

