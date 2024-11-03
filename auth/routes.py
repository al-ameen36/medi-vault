import os
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from supabase import Client
from auth.controller import encode_jwt
from db.controller import get_db
from users.controller import add_user, check_if_exists, get_user_by_email
from users.schemas import UserCreateType, UserType


SECRET = os.environ.get("SECRET")
router = APIRouter()


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Client = Depends(get_db),
):
    user = get_user_by_email(db, email=form_data.username, remove_password=False)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not bcrypt.checkpw(form_data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    encoded_jwt = encode_jwt(user.model_dump())
    del user.password
    return {"access_token": encoded_jwt, "user": user}


@router.post("/user")
async def create_user(user: UserCreateType, db: Client = Depends(get_db)):
    db_user = add_user(db, user)
    return {"response": "User created successfully", "data": db_user}
