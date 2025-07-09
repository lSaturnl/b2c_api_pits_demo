from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.client import Client

app = FastAPI()

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
