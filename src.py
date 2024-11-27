from fastapi import FastAPI
from managment_user import managment_user

app = FastAPI()

app.include_router(managment_user, prefix="/managment_user")