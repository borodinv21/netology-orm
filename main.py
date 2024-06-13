import os
import sqlalchemy
import json

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, aliased
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

    # with open('fixtures/tests_data.json', 'r') as fd:
    #     data = json.load(fd)
    #
    # for record in data:
    #     model = {
    #         'publisher': Publisher,
    #         'shop': Shop,
    #         'book': Book,
    #         'stock': Stock,
    #         'sale': Sale,
    #     }[record.get('model')]
    #     session.add(model(id=record.get('pk'), **record.get('fields')))
    #
    # session.commit()

    session.close()

