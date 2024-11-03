from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from users import routes as user_routes
from auth import routes as auth_routes
from prescriptions import routes as prescription_routes

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    user_routes.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(user_routes.get_current_user)],
)

app.include_router(
    prescription_routes.router,
    prefix="/prescription",
    tags=["prescription"],
    dependencies=[Depends(user_routes.get_current_user)],
)
