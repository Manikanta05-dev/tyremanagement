from pydantic import BaseModel

class ShopConfig(BaseModel):
    shop_name: str = "Tire Shop"
    shop_address: str = "123 Main Street, City, State - 123456"
    gstin: str = "22AAAAA0000A1Z5"
    phone: str = "+91-9876543210"
    email: str = "info@tireshop.com"

class InvoiceGenerateRequest(BaseModel):
    sale_id: int

class WhatsAppSendRequest(BaseModel):
    sale_id: int
    customer_mobile: str
