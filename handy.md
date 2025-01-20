pip freeze | grep -v -E 'black|ruff' > requirements.txt

uvicorn main:app --reload

npm run dev


# When changing the database models
alembic revision --autogenerate -m "description of change"
alembic upgrade head - this will upgrade the database tables
alembic downgrade -1 - this will revert the last upgrade