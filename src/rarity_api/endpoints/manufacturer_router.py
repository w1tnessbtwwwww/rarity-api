from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rarity_api.database import get_session
from rarity_api.endpoints.datas import ManufacturerData, CityData
from rarity_api.endpoints.repos import Manufacturer, ManufacturerRepository

router = APIRouter(
    prefix="/manufacturers",
    tags=["manufacturers"]
)


def mapping(manufacturer: Manufacturer) -> ManufacturerData:
    return ManufacturerData(
        id=manufacturer.id,
        name=manufacturer.name,
        cities=[CityData(id=city.id, name=city.name) for city in manufacturer.cities]
    )

@router.get("/")
async def get_manufacturers(
        session: AsyncSession = Depends(get_session)
) -> List[ManufacturerData]:
    repository = ManufacturerRepository(session)
    manufacturers = await repository.get_by_filter({})
    return [mapping(manufacturer) for manufacturer in manufacturers]
