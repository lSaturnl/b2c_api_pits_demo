from fastapi import APIRouter, Depends, HTTPException, Response, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.shipment import Shipment
from app.schemas.label import LabelRequest
from jinja2 import Environment, FileSystemLoader
import os

router = APIRouter(prefix="/labels", tags=["Labels"])

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates"))

templates = Jinja2Templates(directory=TEMPLATES_DIR)
templates.env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    auto_reload=True,
    cache_size=0
)
template = templates.env.get_template("waybill_10x15.html")



@router.get("/filter", response_class=HTMLResponse)
def render_selected_labels(
    tracking_numbers: list[str] = Query(...),
    db: Session = Depends(get_db)
):
    shipments = db.query(Shipment).filter(Shipment.tracking_number.in_(tracking_numbers)).all()
    if not shipments:
        raise HTTPException(status_code=404, detail="No matching shipments found")

    html = template.render(shipments=shipments)
    return HTMLResponse(content=html)


@router.post("/", response_class=Response)
def generate_labels(data: LabelRequest, db: Session = Depends(get_db)):
    shipments = db.query(Shipment).filter(Shipment.tracking_number.in_(data.tracking_numbers)).all()
    if not shipments:
        raise HTTPException(status_code=404, detail="No shipments found")

    html = template.render(shipments=shipments)

    if data.format == "html":
        return HTMLResponse(content=html)

    elif data.format == "pdf":
        from weasyprint import HTML
        pdf = HTML(string=html).write_pdf()
        return Response(content=pdf, media_type="application/pdf")

    raise HTTPException(status_code=400, detail="Invalid format")
