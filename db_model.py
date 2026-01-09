from sqlalchemy import Column, Integer, String , Float

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):

    __tableName__ = "product"

    id = Column(Integer , primary_key=True , index=True)
    name:str
    description:str
    price:float
    quantity:int