from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import routers
from app.db.session import engine
from app.db.base_class import Base
from app.core.logger import configure_logger, LogLevels
import logging

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tighmrt - backend", description="Tighmrt - Task Manager API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_logger(LogLevels.INFO)

@app.on_event("startup")
def startup():
    logging.info("Starting up...")

@app.on_event("shutdown")
def shutdown():
    logging.info("Shutting down...")

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Tighmrt - Task Manager API"}
    
app.include_router(routers, prefix="/api/v1")
