from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import routers
from app.core.logger import configure_logger, LogLevels
from app.core.config import settings
import logging

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_logger(LogLevels.INFO)


@app.on_event("startup")
async def startup():
    logging.info("Starting up...")


@app.on_event("shutdown")
async def shutdown():
    logging.info("Shutting down...")


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to " + settings.APP_NAME}


app.include_router(routers, prefix="/api/v1")
