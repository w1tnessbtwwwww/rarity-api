from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from rarity_api.database import get_session
from rarity_api.endpoints.datas import ItemData
from rarity_api.endpoints.repos import Item
from rarity_api.endpoints.repos import ItemRepository

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/")
async def get_items(
        session: AsyncSession = Depends(get_session)
) -> List[ItemData]:
    repository = ItemRepository(session)
    items = await repository.get_by_filter({})
    return [mapping(item) for item in items]


@router.get("/{item_id}")
async def get_item(
        item_id: int,
        session: AsyncSession = Depends(get_session)
) -> ItemData:
    repository = ItemRepository(session)
    item = await repository.find_by_id(item_id)
    if not item:
        return Response(status_code=404)
    return mapping(item)


def mapping(item: Item) -> ItemData:
    return ItemData(
        id=item.id,
        name=item.name,
        description=item.description,
        production_years=item.production_years,
        photo_links=item.photo_links
    )


# TODO: FAVS: mark as fav, list all favs, depends on user ofc.
