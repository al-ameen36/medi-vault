import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from db.controller import get_db
from users.controller import (
    delete_user,
    get_current_user,
    get_user,
    get_users,
)
from users.schemas import UserType


SECRET = os.environ.get("SECRET")
router = APIRouter()


def is_doctor(user: UserType = Depends(get_current_user)):
    if not user.role == "doctor":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )
    return True


def is_patient(user: UserType = Depends(get_current_user)):
    if not user.role == "patient":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )
    return True


def is_pharmacy(user: UserType = Depends(get_current_user)):
    if not user.role == "pharmacy":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )
    return True


@router.get("/")
# async def read_users(current_user: Annotated[UserType, Depends(get_current_user)]):
async def read_users(db: Annotated[Client, Depends(get_db)]):
    users = get_users(db)
    return {"detail": "User fetched successfully", "data": users}


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
