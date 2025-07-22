from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers import shipments, labels
from app.database import SessionLocal
from app.models.client import Client
from app.dependencies.startup import init_parcel_number_counter
from fastapi.staticfiles import StaticFiles
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_parcel_number_counter()
    yield
    # Cleanup при завершенні (опціонально)

app = FastAPI(
    title="Api_IPSExpress_B2C",
    description="API for IPS Express (B2C integration)",
    version="0.1.0",
    lifespan=lifespan
)

# Підключення статичних файлів (наприклад, шрифти, CSS)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static"
)

# Підключення роутерів
app.include_router(shipments.router)
app.include_router(labels.router)

# Залежність для роботи з БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API працює!"}

@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    client = db.query(Client).first()
    return {"status": "ok", "has_clients": bool(client)}  # TEST
