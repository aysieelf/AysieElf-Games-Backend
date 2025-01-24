pip freeze | grep -v -E 'black|ruff' > requirements.txt

uvicorn main:app --reload

npm run dev


# When changing the database models
1. Drop the schema and recreate it
```bash
heroku pg:psql --app aysieelf-games-db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```
2. Delete migrations
3. Create new migrations
```bash
atlas migrate diff new_changes --env postgresql
atlas migrate apply --env postgresql --allow-dirty
```