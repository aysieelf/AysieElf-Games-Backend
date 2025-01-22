from src.models.base import Base

from atlas_provider_sqlalchemy.ddl import print_ddl

# Тук използваме postgresql вместо mysql
print_ddl("postgresql", [Base])
