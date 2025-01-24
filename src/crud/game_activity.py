from src.models import GameActivity
from src.schemas.game_activity import GameActivityRead


def _convert_to_game_activity_read(activity: GameActivity) -> GameActivityRead:
    return GameActivityRead(
        id=activity.id,
        user_id=activity.user_id,
        game_id=activity.game_id,
        played_at=activity.played_at,
    )