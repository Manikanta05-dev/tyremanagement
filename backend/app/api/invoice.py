from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.services.invoice_service import InvoiceService
from app.services.whatsapp_service import WhatsAppService
from app.models.user import User
import os

router = APIRouter(prefix="/invoice", tags=["Invoice"])

@router.get("/generate/{sale_id}")
def generate_invoice(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice_service = InvoiceService(db)
    filename = invoice_service.generate_invoice_pdf(sale_id)
    
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Invoice file not found")
    
    return FileResponse(
        filename,
        media_type='application/pdf',
        filename=os.path.basename(filename)
    )

@router.post("/send-whatsapp/{sale_id}")
def send_invoice_whatsapp(
    sale_id: int,
    customer_mobile: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Generate invoice first
    invoice_service = InvoiceService(db)
    filename = invoice_service.generate_invoice_pdf(sale_id)
    
    # Get sale details for invoice ID
    from app.repositories.sales_repository import SalesRepository
    sales_repo = SalesRepository(db)
    sale = sales_repo.get_by_id(sale_id)
    
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Send via WhatsApp
    whatsapp_service = WhatsAppService()
    result = whatsapp_service.send_invoice(customer_mobile, filename, sale.invoice_id)
    
    return result
