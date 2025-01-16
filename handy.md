pip freeze | grep -v -E 'black|ruff' > requirements.txt

uvicorn main:app --reload

npm run dev