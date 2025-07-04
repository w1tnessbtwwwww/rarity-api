from typing import Union
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
import openpyxl
from pydantic import BaseModel

from rarity_api.common.auth.native_auth.dependencies import authenticate
from rarity_api.common.auth.schemas.user import UserRead
from rarity_api.core.database.connector import get_session
from rarity_api.core.database.repos.repos import CityRepository, CountryRepository, ItemRepository, ManufacturerRepository, RegionRepository

import zipfile
import tempfile

import os
import shutil
from fastapi import HTTPException, UploadFile, File
from openpyxl import load_workbook
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/excel",
    tags=["excel"]
)

class ReadItem(BaseModel):
    rp: int | None
    country: str | None
    manufacturer_name: str | None
    region: str | None
    city: str | None
    prod_year_start: int | None
    prod_year_end: Union[int, str] | None
    desc: str | None

EXCEL_PROCESSING_DIR = "excels"  # Папка для обработки Excel
IMAGES_DIR = "images"  # Папка для изображений
os.makedirs(IMAGES_DIR, exist_ok=True)

async def process_excel_file(session: AsyncSession, excel_path: str):
    """Обработка Excel файла и сохранение в БД"""
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=10, values_only=True):
        # Пропускаем пустые строки
        if not row[0]:
            continue
            
        current_row = ReadItem(
            rp=row[0],
            country=row[1],
            manufacturer_name=row[2],
            region=row[3],
            city=row[4],
            prod_year_start=row[5],
            prod_year_end=row[6],
            desc=row[7]
        )

        country_repository = CountryRepository(session)
        city_repository = CityRepository(session)
        region_repository = RegionRepository(session)
        manufacturer_repository = ManufacturerRepository(session)
        item_repository = ItemRepository(session)

        country = await country_repository.get_or_create(name=current_row.country)
        region = await region_repository.get_or_create(name=current_row.region, country_id=country.id)
        city = await city_repository.get_or_create(name=current_row.city, region_id=region.id if region else None)
        manufacturer = await manufacturer_repository.get_or_create(name=current_row.manufacturer_name)
        
        # Форматируем строку с годами
        year_end = current_row.prod_year_end if current_row.prod_year_end else "now"
        production_years = f"{current_row.prod_year_start} - {year_end}"

        await item_repository.create(
            rp=current_row.rp,
            manufacturer_id=manufacturer.id,
            description=current_row.desc,
            production_years=production_years
        )

@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    user: UserRead = Depends(authenticate),
    excel_dir: str = EXCEL_PROCESSING_DIR,  # Можете передать свой путь
    images_dir: str = IMAGES_DIR,
    session: AsyncSession = Depends(get_session)  # Можете передать свой путь
):
    """
    Загрузка архива с Excel и изображениями
    
    Параметры:
    - excel_dir: путь для сохранения Excel файлов (по умолчанию 'excels')
    - images_dir: путь для сохранения изображений (по умолчанию 'static/marks_images')
    """
    # Создаем временную директорию
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Проверяем и распаковываем архив
            with zipfile.ZipFile(file.file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        except zipfile.BadZipFile:
            raise HTTPException(400, detail="Невозможно распаковать архив. Файл поврежден.")
        
        # Поиск Excel-файла
        excel_path = None
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                if file_name.endswith('.xlsx'):
                    excel_path = os.path.join(root, file_name)
                    break
            if excel_path:
                break
        
        if not excel_path:
            raise HTTPException(400, detail="Excel файл (.xlsx) не найден в архиве")
        
        # Поиск папки с изображениями
        images_source = None
        for root, dirs, _ in os.walk(temp_dir):
            if 'book' in dirs:
                book_path = os.path.join(root, 'book')
                marks_path = os.path.join(book_path, 'marks_images')
                if os.path.exists(marks_path):
                    images_source = marks_path
                    break
        
        if not images_source:
            raise HTTPException(400, detail="Папка book/marks_images не найдена в архиве")
        
        # Обработка изображений
        if os.path.exists(images_dir):
            shutil.rmtree(images_dir)
        shutil.copytree(images_source, images_dir)
        
        # Обработка Excel
        try:
            # Создаем сессию для работы с БД
            await process_excel_file(session, excel_path)
            
            return {
                "status": "success",
                "message": "Excel файл и изображения успешно обработаны",
                "excel_path": excel_path,
                "images_dir": images_dir
            }
        
        except Exception as e:
            raise HTTPException(500, detail=f"Ошибка обработки Excel: {str(e)}")
        