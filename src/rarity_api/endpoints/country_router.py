from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rarity_api.database import get_session
from rarity_api.endpoints.datas import CountryData
from rarity_api.endpoints.repos import Country, CountryRepository

router = APIRouter(
    prefix="/countries",
    tags=["countries"]
)


def mapping(country: Country) -> CountryData:
    return CountryData(
        id=country.id,
        name=country.name
    )


@router.get("/")
async def get_countries(
        name: str = None,
        session: AsyncSession = Depends(get_session)
) -> List[CountryData]:
    repository = CountryRepository(session)
    countries: List[Country] = await repository.get_by_filter({})
    return [mapping(country) for country in countries]
