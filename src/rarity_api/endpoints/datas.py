from pydantic import BaseModel
from datetime import datetime


class CityData(BaseModel):
    id: int
    name: str  # nullable=False
    # region_id: int  # nullable=False
    # region: RegionData
    # manufacturers: list[ManufacturerData]


class RegionData(BaseModel):
    id: int
    name: str  # nullable=False
    # country_id: int
    # country: CountryData
    # cities: list[CityData]


class CountryData(BaseModel):
    id: int
    name: str  # nullable=False
    # regions: list[RegionData]


class ManufacturerData(BaseModel):
    id: int
    name: str  # nullable=False
    cities: list[CityData]
    # items: list[ItemData]


class ItemData(BaseModel):
    id: int
    name: str  # nullable=False
    description: str  # nullable=True
    image: str
    date_from: str  # Можно хранить как JSON или просто строку с диапазонами
    date_to: str  # Можно хранить как JSON или просто строку с диапазонами
    is_favourite: bool  # nullable!
    # manufacturer_id: int
    # manufacturer: ManufacturerData


class ItemFullData(ItemData):
    country: str
    region: str
    city: str
    manufacturer: str


class SearchHistoryData(BaseModel):
    id: int
    region_name: str | None
    country_name: str | None
    manufacturer_name: str | None
    created_at: datetime


class SearchHistoryCreate(BaseModel):
    region_name: str | None = None
    country_name: str | None = None
    manufacturer_name: str | None = None
