from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.authentication import get_current_user
from src.crud.user import update_password
from src.schemas.user import UserUpdate

router = APIRouter()

@router.put("/password")
def reset_password(
    new_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return update_password(new_user.password, db, current_user)
