from typing import List

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from rarity_api.endpoints.datas import ItemData, SearchHistoryCreate, ItemFullData, FindByImageData

from rarity_api.core.database.connector import get_session
from rarity_api.core.database.models.models import Item, SearchHistory
from rarity_api.core.database.repos.repos import ItemRepository, SearchHistoryRepository
from rarity_api.settings import settings

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/")
async def get_items(
        page: int = 1,
        offset: int = 50,
        region_name: str = None,
        country_name: str = None,
        manufacturer_name: str = None,
        # from_date: str = None,
        # to_date: str = None,
        session: AsyncSession = Depends(get_session)
) -> List[ItemData]:
    # Save search history
    search_history = SearchHistory(
#        region_name=region_name,
        region_name=region_name if region_name else "Bayern",
        country_name=country_name,
        manufacturer_name=manufacturer_name
    )
    history_repository = SearchHistoryRepository(session)
    await history_repository.create(search_history)
    repository = ItemRepository(session)
    items = await repository.find_items(page, offset, region=region_name, country=country_name, manufacturer=manufacturer_name)
    return [mapping(item) for item in items]


@router.get("/{item_id}")
async def get_item(
        item_id: int,
        session: AsyncSession = Depends(get_session)
) -> ItemFullData:
    repository = ItemRepository(session)
    item = await repository.find_by_id(item_id)
    if not item:
        return Response(status_code=404)
    return mapping(item)



@router.put("/{item_id}/markfav")
async def mark_favourite(
        item_id: int,
        session: AsyncSession = Depends(get_session)
) -> ItemData:
    repository = ItemRepository(session)
    item = await repository.find_by_id(item_id)
    if not item:
        return Response(status_code=404)
    return mapping(item)


@router.get("/favourites")
async def list_favourites(
        session: AsyncSession = Depends(get_session)
) -> List[ItemData]:
    repository = ItemRepository(session)
    # ...
    # return [mapping(item) for item in items]


@router.post("/find_by_image")
async def find_by_image(
        data: FindByImageData,
        session: AsyncSession = Depends(get_session)
):
    response = requests.post(
        # TODO: use env for llm URL
        'http://158.255.6.121:8080/recognize',
        json={'image': data.base64}
    )
    if response.status_code != 200:
        return Response(status_code=response.status_code)
    data = response.json()
    if data['status'] != 'success':
        return Response(status_code=400)
    results = data['results'] if data['results'] else []
    sorted_by_similarity = sorted(results, key=lambda d: d['similarity'])
    print(sorted_by_similarity)
    repository = ItemRepository(session)
    a = []
    for result in sorted_by_similarity:
        i = int(result['template'].split('/')[-1].split('_')[1].split('.')[0])
        item = await repository.find_by_book_id(i)
        if item:
            item_data = mapping(item)
            a.append(item_data)
    return a


def mapping(item: Item) -> ItemData:

    years_array = item.production_years.split(" - ")
    years_end = int(years_array[1] if years_array[1] != "now" else 0)
    print(years_array)

    return ItemData(
        id=item.id,
        rp=item.rp,
        name=item.name,
        description=item.description,
        year_from=int(years_array[0] if years_array[0] != "None" else 0),
        year_to=years_end,
        image=f"{settings.api_base_url}/images/mark_{item.rp}.png" if item.rp else None,
    )
