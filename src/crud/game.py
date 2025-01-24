from src.models import Game
from src.schemas.game import GameReadAll


def _convert_to_game_read_all(game: Game) -> GameReadAll:
    return GameReadAll(
        id=game.id,
        title=game.title,
        slug=game.slug,
        icon=game.icon,
        description=game.description,
        category_slug=game.category.slug,
        category_title=game.category.title,
    )
