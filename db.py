from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///airbnb.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
