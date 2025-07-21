from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.shipment import Shipment
from app.schemas.label import LabelRequest
from app.templates import templates  # імпортуємо єдиний інстанс

router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("/filter", response_class=HTMLResponse)
def render_selected_labels(
    request: Request,
    tracking_numbers: list[str] = Query(...),
    db: Session = Depends(get_db)
):
    shipments = db.query(Shipment).filter(Shipment.tracking_number.in_(tracking_numbers)).all()
    if not shipments:
        raise HTTPException(status_code=404, detail="No matching shipments found")
    return templates.TemplateResponse("waybill_10x15.html", {
        "request": request,
        "shipments": shipments
    })

@router.post("/", response_class=Response)
def generate_labels(
    request: Request,
    data: LabelRequest,
    db: Session = Depends(get_db)
):
    shipments = db.query(Shipment).filter(Shipment.tracking_number.in_(data.tracking_numbers)).all()
    if not shipments:
        raise HTTPException(status_code=404, detail="No shipments found")

    if data.format == "html":
        return templates.TemplateResponse("waybill_10x15.html", {
            "request": request,
            "shipments": shipments
        })

    elif data.format == "pdf":
        html = templates.get_template("waybill_10x15.html").render({
            "request": request,
            "shipments": shipments
        })
        from weasyprint import HTML as WHTML
        pdf = WHTML(string=html, base_url=request.base_url).write_pdf()
        return Response(content=pdf, media_type="application/pdf")

    raise HTTPException(status_code=400, detail="Invalid format")
