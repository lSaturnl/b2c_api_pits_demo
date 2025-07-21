from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routers import shipments, labels

from app.database import SessionLocal
from app.models.client import Client
from app.dependencies.startup import init_parcel_number_counter
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_parcel_number_counter()  # <- виконується при запуску
    yield
    # тут можна cleanup, якщо треба

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(shipments.router)
app.include_router(labels.router)

# Dependency для отримання сесії
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
    # Перевіримо, чи можемо прочитати хоча б 1 клієнта
    client = db.query(Client).first()
    return {"status": "ok", "has_clients": bool(client)}
# TEST