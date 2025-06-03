from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from rarity_api.endpoints.datas import RegionData

from rarity_api.core.database.connector import get_session
from rarity_api.core.database.models.models import Region
from rarity_api.core.database.repos.repos import RegionRepository

router = APIRouter(
    prefix="/regions",
    tags=["regions"]
)


def mapping(region: Region) -> RegionData:
    return RegionData(
        id=region.id,
        name=region.name
    )

@router.get("/")
async def get_regions(
        name: str = None,
        session: AsyncSession = Depends(get_session)
) -> List[RegionData]:
    repository = RegionRepository(session)
    regions: Sequence[Region] = await repository.find_by_filter(name)
    return [mapping(region) for region in regions]
