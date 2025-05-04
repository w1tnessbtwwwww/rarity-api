from datetime import datetime
from typing import Dict, Any, Sequence

from sqlalchemy import Column, Integer, String, ForeignKey, Table, select, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Определяем таблицу для связи многие-ко-многим между Производителем и Городом
manufacturer_city_association = Table(
    'manufacturer_city', Base.metadata,
    Column('manufacturer_id', Integer, ForeignKey('manufacturers.id'), primary_key=True),
    Column('city_id', Integer, ForeignKey('cities.id'), primary_key=True)
)


class BaseRepository:
    # model_class = declarativebase + id
    def __init__(self, session: AsyncSession, model_class):
        self.session = session
        self.model_class = model_class

    async def get_by_filter(self, filters: Dict[str, Any]) -> Sequence[Any]:
        query = select(self.model_class)
        for key, value in filters.items():
            query = query.where(getattr(self.model_class, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id_: int) -> Any:
        query = select(self.model_class).where(self.model_class.id == id_)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: Dict[str, Any]) -> Any:
        instance = self.model_class(**data)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update(self, id: int, data: Dict[str, Any]) -> Any:
        instance = await self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            await self.session.commit()
        return instance

    async def delete(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
            return True
        return False


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # regions = relationship("Region", back_populates="country")


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    # country = relationship("Country", back_populates="regions")
    # cities = relationship("City", back_populates="region")


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    # region = relationship("Region", back_populates="cities")
    # manufacturers = relationship("Manufacturer", secondary=manufacturer_city_association, back_populates="cities")


class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # cities = relationship("City", secondary=manufacturer_city_association, back_populates="manufacturers")
    # items = relationship("Item", back_populates="manufacturer")


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    # production_years = Column(String)  # Можно хранить как JSON или просто строку с диапазонами
    # photo_links = Column(String)  # Можно хранить ссылки в формате JSON
    # manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=False)
    # manufacturer = relationship("Manufacturer", back_populates="items")


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)
    region_name = Column(String, nullable=True)
    country_name = Column(String, nullable=True)
    manufacturer_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CountryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Country)


class RegionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Region)


class CityRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, City)


class ManufacturerRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Manufacturer)


class ItemRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Item)


class SearchHistoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SearchHistory)
