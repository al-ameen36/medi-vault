import os
from typing import Annotated
from fastapi import APIRouter, Depends
from supabase import Client
from db.controller import get_db
from users.controller import (
    delete_user,
    get_current_user,
    get_user,
)
from users.schemas import UserType


SECRET = os.environ.get("SECRET")
router = APIRouter()


@router.get("/me")
async def read_users_me(current_user: Annotated[UserType, Depends(get_current_user)]):
    return {"detail": "User fetched successfully", "data": current_user}


@router.get("/{user_id}")
def read_user(user_id: int, db: Client = Depends(get_db)):
    user = get_user(db, user_id)
    return {
        "detail": "User fetched successfully",
        "data": user.to_pydantic(no_password=True),
    }


@router.delete("/{user_id}/delete")
async def delete_users_me(
    user_id: int,
    db: Client = Depends(get_db),
):
    delete_user(db, user_id)
    return {"detail": "User deleted successfully"}
