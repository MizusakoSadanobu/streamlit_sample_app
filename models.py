from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    properties = relationship("Property", back_populates="owner")
    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    availability = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="properties")
    bookings = relationship("Booking", back_populates="property")
    reviews = relationship("Review", back_populates="property")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    date = Column(Date)
    user = relationship("User", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    review_text = Column(String)
    date = Column(Date)
    user = relationship("User", back_populates="reviews")
    property = relationship("Property", back_populates="reviews")
