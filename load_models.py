from src.models.base import Base
from src.models.user import User
from src.models.blacklisted_token import BlacklistedToken
from src.models.friendship import Friendship
from src.models.game import Game
from src.models.game_activity import GameActivity
from src.models.upvote import Upvote
from src.models.favorite import Favorite
from src.models.category import Category
from atlas_provider_sqlalchemy.ddl import print_ddl

# Тук използваме postgresql вместо mysql
print_ddl("postgresql", [Base])