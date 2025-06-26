import asyncio
import sqlite3
import re

from rarity_api.core.database.connector import get_session

# --- Подключение к базе ---
# conn = sqlite3.connect("symbols.db")
# cursor = conn.cursor()
#
# cursor.execute("DROP TABLE IF EXISTS symbols")
# cursor.execute("""
# CREATE TABLE symbols (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     image_number INTEGER NOT NULL
# )
# """)
# conn.commit()

# --- Чтение из файла ---
entries = []
with open("excels/symbol_index.txt", "r", encoding="utf-8") as file:
    buffer = ""
    for line in file:
        line = line.strip()
        if not line:
            continue  # пропускаем пустые строки
        if re.search(r'\d', line) and not re.match(r'^\d', line):  # начало новой записи
            if buffer:
                entries.append(buffer)
            buffer = line
        else:
            buffer += " " + line
    if buffer:
        entries.append(buffer)

# --- Парсинг диапазонов и чисел ---
def parse_numbers(part):
    numbers = []
    for token in re.split(r',\s*', part):
        if '-' in token:
            try:
                start, end = map(int, token.split('-'))
                numbers.extend(range(start, end + 1))
            except ValueError:
                pass
        else:
            try:
                numbers.append(int(token))
            except ValueError:
                pass
    return numbers


async def main():
    async for session in get_session():
        # --- Загрузка в базу ---
        for entry in entries:
            match = re.match(r'^(.+?)\s+([\d,\-\s]+)$', entry)
            if not match:
                print(f"❌ Не удалось разобрать: {entry}")
                continue
            name = match.group(1).strip()
            nums = parse_numbers(match.group(2))
            print(nums)
            # for num in nums:
            #     cursor.execute("INSERT INTO symbols (name, image_number) VALUES (?, ?)", (name, num))
        # conn.commit()


if __name__ == "__main__":
    asyncio.run(main())
