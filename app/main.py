from fastapi import FastAPI
from app.api.v1.router import router

app = FastAPI(title="Retail AI Advisor")

app.include_router(router)
