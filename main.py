from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
import database.router
import authorization.router


app = FastAPI()


app.include_router(database.router.router)
app.include_router(authorization.router.router)
