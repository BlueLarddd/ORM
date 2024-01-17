import pymysql

from sqlalchemy import Integer, String, Column, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from prettytable import PrettyTable

engine = create_engine(f'mysql+pymysql://student:Hn523cv-@95.154.68.63:3306/[Prodivers_LD_DB]')

session = Session(bind=engine)

Base = declarative_base()

products = Table('products', Base.metadata,
    Column('category_id', Integer(), ForeignKey("categories.id")),
    Column('storage_id', Integer(), ForeignKey("storage.id")),
)

class Prod(Base):
    tablename = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    storage_id = Column(Integer, ForeignKey('storage.id'))

    def add_type(self, type_name):
        t = Prod(name=type_name)
        session.add(t)
        session.commit()

    def get_type(self):
        query = text('SELECT * FROM products')
        result = session.execute(query)
        t = PrettyTable(['id', 'name', 'price', 'category_id', 'storage_id'])
        for row in result:
            t.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(f'\n{t}\n')

    def upd_type(self, old_type_name, new_type_name):
        t = session.query(Prod).filter(Prod.name == old_type_name).one()
        t = t.id
        ty = session.query(Prod).get(t)
        ty.name = new_type_name
        session.add(ty)
        session.commit()

    def del_type(self, type_name):
        t = session.query(Prod).filter(Prod.name == type_name).one()
        session.delete(t)
        session.commit()

# class Cat(Base):
#     tablename = 'categories'
#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     name = Column(String(255), nullable=False)
#
#     def add_ingridient(self, dish, product, weight):
#         d = session.query(Cat).filter(Cat.name == dish).one()
#         d = d.id
#         di = session.query(Cat).get(d)
#         p = session.query(Product).filter(Product.name == product).one()
#         p = p.id
#         pr = session.query(Product).get(p)
#
#         ing = ingridients_for_dish.insert().values(dish_id=d, product_id=p, weight=weight)
#         session.add_all([di, pr])
#         session.execute(ing)
#         session.commit()
#
#     def get_ingridients_for_dish(self, dish_name):
#         d = session.query(Dish).filter(Dish.name == dish_name).one()
#         d = d.id
#
#         query = text(f'SELECT name FROM products WHERE id in (SELECT product_id FROM ingridients_for_dish WHERE dish_id = {d})')
#         result = session.execute(query)
#         t = PrettyTable(['product_name'])
#         for row in result:
#             t.add_row([row[0]])
#         print("\nDish's name:")
#         print(f"> {dish_name}")
#         print(f'{t}\n')
#
#     def add_dish(self, name, type, base, output_in_grams):
#         t = session.query(Type_of_dishes).filter(Type_of_dishes.name == type).one()
#         t = t.id
#         ty = session.query(Type_of_dishes).get(t)
#         d = Dish(name=name, type_id=t, base=base, output_in_grams=output_in_grams)
#         session.add_all([ty, d])
#         session.commit()
#
#     def get_dishes(self):
#         query = text('SELECT * FROM dishes')
#         result = session.execute(query)
#         t = PrettyTable(['id', 'name', 'type_id', 'base', 'output_in_grams'])
#         for row in result:
#             t.add_row([row[0], row[1], row[2], row[3], row[4]])
#         print(f'\n{t}\n')
#
#     def upd_dish(self, old_dish_name, new_dish_name):
#         d = session.query(Dish).filter(Dish.name == old_dish_name).one()
#         d = d.id
#         di = session.query(Dish).get(d)
#         di.name = new_dish_name
#         session.add(di)
#         session.commit()