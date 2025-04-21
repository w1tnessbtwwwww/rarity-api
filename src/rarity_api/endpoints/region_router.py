from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rarity_api.database import get_session
from rarity_api.endpoints.datas import RegionData
from rarity_api.endpoints.repos import Region, RegionRepository

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
        session: AsyncSession = Depends(get_session)
) -> List[RegionData]:
    repository = RegionRepository(session)
    regions: List[Region] = await repository.get_by_filter({})
    return [mapping(region) for region in regions]
