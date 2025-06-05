from pydantic import BaseModel
from datetime import datetime
from pydantic import field_validator
from rarity_api.settings import settings
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
    name: str | None = None  # nullable=False
    description: str | None = None  # nullable=True
    image: str | None = None
    year_from: int | None = None
    year_to: int | None = None
    is_favourite: bool = False  # nullable!
    photo_link: str | None = None

    @field_validator("photo_link")
    def validate_photo(cls, value):
        return f"{settings.images_dir_path}/"
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
