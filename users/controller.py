from typing import Annotated
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import Client
from auth.controller import decode_jwt
from users.routes import get_db
from users.schemas import UserCreateType, UserType


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_users(db: Client):
    user = db.table("users").select("*").execute()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return [UserType(**user) for user in user.data]


def get_user(db: Client, user_id: int):
    user = db.table("users").select("*").eq("id", user_id).execute()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def check_if_exists(db: Client, email: int):
    try:
        user = db.table("users").select("id").eq("email", email).execute()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=404, detail="User not found")

    return bool(len(user.data))


def get_user_by_email(db: Client, email: int, remove_password: bool = True):
    try:
        user = db.table("users").select("*").eq("email", email).single().execute()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=404, detail="User not found")

    if remove_password:
        return UserType(**user.data)
    else:
        return UserCreateType(**user.data)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Client = Depends(get_db)
):
    if "null" in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user = decode_jwt(token)
        user = get_user_by_email(db, email=user["email"])
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def add_user(db: Client, user: UserCreateType):
    user_exists = check_if_exists(db, user.email)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    try:
        payload = {**user.model_dump(), "password": hashed_password.decode()}
        db_user = db.table("users").insert(payload).execute()

        return UserType(**db_user.data[0])
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail="Could not create user")


def delete_user(db: Client, user_id: int):
    get_user(db, user_id=user_id)

    db.table("users").delete().eq("id", user_id).execute()
    return True
