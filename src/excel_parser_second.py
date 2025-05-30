import asyncio
import os
from typing import Union

import openpyxl
from pydantic import BaseModel, field_validator

from rarity_api.core.database.connector import get_session
from rarity_api.core.database.repos.repos import (
    CityRepository,
    CountryRepository,
    ItemRepository,
    ManufacturerRepository,
    RegionRepository,
)


class ReadItem(BaseModel):
    img: str | None = None
    country: str | None = None
    manufacturer_name: str | None = None
    region: str | None = None
    city: str | None = None
    prod_year_start: int | None = None
    prod_year_end: Union[int, str] | None = None
    desc: str | None = None
    name: str | None = None

    @field_validator('country')
    def validate_country(cls, value):
        return value.split("/")[0] if "/" in value else value


async def main():
    async for session in get_session():
        path = os.path.join(os.path.dirname(__file__), 'excels\\porzellanmarken.xlsx')

        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=10, values_only=True):
            current_row = ReadItem(
                name=row[1],
                img=row[2],
                manufacturer_name=row[3],
                prod_year_start=row[4],
                prod_year_end=row[5],
                city=row[6],
                country=row[7],
                desc=row[8]
            )

            print(current_row)


            country_repository = CountryRepository(session)
            city_repository = CityRepository(session)
            region_repository = RegionRepository(session)
            manufacturer_repository = ManufacturerRepository(session)

            item_repository = ItemRepository(session)

            country = await country_repository.get_or_create(name=current_row.country)
            print(country)

            region = await region_repository.get_or_create(name=current_row.region, country_id=country.id)
            city = await city_repository.get_or_create(name=current_row.city, region_id=region.id if region else None)
            manufacturer = await manufacturer_repository.get_or_create(name=current_row.manufacturer_name)
            
            item = await item_repository.create(
                manufacturer_id=manufacturer.id,
                name=current_row.name,
                photo_links=current_row.img,
                description=current_row.desc,
                production_years=f"{current_row.prod_year_start} - {current_row.prod_year_end if current_row.prod_year_end else "now"}"
            )

if __name__ == "__main__":
    asyncio.run(main())
