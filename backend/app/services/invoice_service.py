from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
import os
from app.repositories.sales_repository import SalesRepository
from app.schemas.invoice import ShopConfig

class InvoiceService:
    def __init__(self, db: Session):
        self.sales_repo = SalesRepository(db)
        self.shop_config = ShopConfig()
        
        # Create invoices directory if not exists
        os.makedirs("invoices", exist_ok=True)
    
    def generate_invoice_pdf(self, sale_id: int) -> str:
        # Get sale details
        sale = self.sales_repo.get_by_id(sale_id)
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found"
            )
        
        # Create PDF filename
        filename = f"invoices/invoice_{sale.invoice_id}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a56db'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Shop Header
        elements.append(Paragraph(self.shop_config.shop_name, title_style))
        elements.append(Paragraph(self.shop_config.shop_address, header_style))
        elements.append(Paragraph(f"GSTIN: {self.shop_config.gstin}", header_style))
        elements.append(Paragraph(f"Phone: {self.shop_config.phone} | Email: {self.shop_config.email}", header_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice Title
        invoice_title = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a56db'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        elements.append(Paragraph("TAX INVOICE", invoice_title))
        elements.append(Spacer(1, 0.2*inch))
        
        # Invoice Details
        invoice_data = [
            ['Invoice No:', sale.invoice_id, 'Date:', sale.sale_date.strftime('%d-%m-%Y')],
            ['Customer:', sale.customer_name, 'Mobile:', sale.customer_mobile],
            ['Payment Mode:', sale.payment_mode.upper(), '', '']
        ]
        
        invoice_table = Table(invoice_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 2*inch])
        invoice_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(invoice_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Items Table
        items_data = [['#', 'Item Description', 'Qty', 'Rate', 'Amount']]
        
        subtotal = 0
        for idx, item in enumerate(sale.items, 1):
            items_data.append([
                str(idx),
                f"{item.tire.brand} - {item.tire.tire_size}",
                str(item.quantity),
                f"₹{item.unit_price:.2f}",
                f"₹{item.total_price:.2f}"
            ])
            subtotal += item.total_price
        
        # Calculate GST
        cgst = subtotal * 0.09  # 9% CGST
        sgst = subtotal * 0.09  # 9% SGST
        grand_total = subtotal + cgst + sgst
        
        # Add GST rows
        items_data.append(['', '', '', 'Subtotal:', f"₹{subtotal:.2f}"])
        items_data.append(['', '', '', 'CGST (9%):', f"₹{cgst:.2f}"])
        items_data.append(['', '', '', 'SGST (9%):', f"₹{sgst:.2f}"])
        items_data.append(['', '', '', 'Grand Total:', f"₹{grand_total:.2f}"])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3.5*inch, 0.8*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a56db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('FONTNAME', (0, 1), (-1, -5), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -5), 10),
            ('GRID', (0, 0), (-1, -5), 1, colors.grey),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Totals section
            ('FONTNAME', (3, -4), (-1, -1), 'Helvetica-Bold'),
            ('LINEABOVE', (3, -4), (-1, -4), 1, colors.grey),
            ('LINEABOVE', (3, -1), (-1, -1), 2, colors.black),
            ('FONTSIZE', (3, -1), (-1, -1), 12),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Thank you for your business!", footer_style))
        elements.append(Paragraph("This is a computer-generated invoice", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        return filename
