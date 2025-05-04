```shell
poetry run uvicorn main:app --reload
```

```shell
alembic revision --autogenerate -m "Add search history table"
alembic upgrade head
```
