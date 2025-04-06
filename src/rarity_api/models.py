from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Определяем таблицу для связи многие-ко-многим между Производителем и Городом
manufacturer_city_association = Table(
    'manufacturer_city', Base.metadata,
    Column('manufacturer_id', Integer, ForeignKey('manufacturers.id'), primary_key=True),
    Column('city_id', Integer, ForeignKey('cities.id'), primary_key=True)
)


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    regions = relationship("Region", back_populates="country")


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship("Country", back_populates="regions")
    cities = relationship("City", back_populates="region")


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    region = relationship("Region", back_populates="cities")
    manufacturers = relationship("Manufacturer", secondary=manufacturer_city_association, back_populates="cities")


class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cities = relationship("City", secondary=manufacturer_city_association, back_populates="manufacturers")
    items = relationship("Item", back_populates="manufacturer")


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    production_years = Column(String)  # Можно хранить как JSON или просто строку с диапазонами
    photo_links = Column(String)  # Можно хранить ссылки в формате JSON
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=False)
    manufacturer = relationship("Manufacturer", back_populates="items")
