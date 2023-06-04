from fastapi import FastAPI
import database.router

app = FastAPI()


app.include_router(database.router.router)
