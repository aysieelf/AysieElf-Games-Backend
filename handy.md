pip freeze | grep -v -E 'black|ruff' > requirements.txt

uvicorn main:app --reload

npm run dev


# When changing the database models
atlas migrate diff new_changes --env postgresql
atlas migrate apply --env postgresql --allow-dirty
