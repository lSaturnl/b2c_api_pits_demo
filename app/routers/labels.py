import os
import base64
from pathlib import Path

import pdfkit
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.shipment import Shipment
from app.schemas.label import LabelRequest
from app.templates import templates  # Jinja2Templates instance

router = APIRouter(prefix="/labels", tags=["Labels"])
config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
font_bytes = Path("app/static/fonts/code128.ttf").read_bytes()
font_base64 = base64.b64encode(font_bytes).decode("utf-8")
font_path = f"data:font/ttf;base64,{font_base64}"

@router.get("/filter")
def render_selected_labels(
        request: Request,
        tracking_numbers: list[str] = Query(...),
        format: str = Query("html", enum=["html", "pdf"]),
        db: Session = Depends(get_db)
    ):
    shipments = db.query(Shipment).filter(Shipment.tracking_number.in_(tracking_numbers)).all()
    if not shipments:
        raise HTTPException(status_code=404, detail="No matching shipments found")

    context = {
        "request": request,
        "shipments": shipments,
        "font_path": font_path if format == "pdf" else None,
    }

    if format == "html":
        return templates.TemplateResponse("waybill_10x15.html", context)

    # PDF generation
    html_string = templates.get_template("waybill_10x15.html").render(context)
    with open("debug_output.html", "w", encoding="utf-8") as f:
        f.write(html_string)
    base_url = str(Path(__file__).parent.parent.absolute())
    pdf = pdfkit.from_string(
        html_string,
        False,
        configuration=config,
        options={
            "page-width": "100mm",
            "page-height": "150mm",
            'margin-top': '1mm',
            'margin-bottom': '0',
            'margin-left': '1mm',
            'margin-right': '0',
            "encoding": "UTF-8",
            "zoom": "1.0",
            "disable-smart-shrinking": "",
        }
    )
    return Response(content=pdf, media_type="application/pdf")

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
