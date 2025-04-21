from pydantic import BaseModel


class CityData(BaseModel):
    id: int
    name: str  # nullable=False
    # region_id: int  # nullable=False
    # region: RegionData
    # manufacturers: list[ManufacturerData]


class RegionData(BaseModel):
    id: id
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
    production_years: str  # Можно хранить как JSON или просто строку с диапазонами
    photo_links: str  # Можно хранить ссылки в формате JSON
    # manufacturer_id: int
    # manufacturer: ManufacturerData
