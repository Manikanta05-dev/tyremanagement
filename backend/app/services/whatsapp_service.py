from twilio.rest import Client
from fastapi import HTTPException, status
import os
from app.core.config import settings

class WhatsAppService:
    def __init__(self):
        # Get Twilio credentials from environment
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    def send_invoice(self, customer_mobile: str, invoice_path: str, invoice_id: str) -> dict:
        """Send invoice via WhatsApp"""
        
        if not self.client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="WhatsApp service not configured. Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env"
            )
        
        try:
            # Format mobile number for WhatsApp
            if not customer_mobile.startswith('+'):
                customer_mobile = f"+91{customer_mobile}"
            
            whatsapp_to = f"whatsapp:{customer_mobile}"
            
            # Send message with invoice
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                to=whatsapp_to,
                body=f"Thank you for your purchase! Here is your invoice {invoice_id}.",
                media_url=[f"https://yourdomain.com/{invoice_path}"]  # Update with your domain
            )
            
            return {
                "success": True,
                "message": "Invoice sent successfully via WhatsApp",
                "message_sid": message.sid
            }
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send WhatsApp message: {str(e)}"
            )
    
    def send_text_message(self, customer_mobile: str, message_text: str) -> dict:
        """Send text message via WhatsApp"""
        
        if not self.client:
            return {
                "success": False,
                "message": "WhatsApp service not configured. Set TWILIO credentials in .env"
            }
        
        try:
            # Format mobile number
            if not customer_mobile.startswith('+'):
                customer_mobile = f"+91{customer_mobile}"
            
            whatsapp_to = f"whatsapp:{customer_mobile}"
            
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                to=whatsapp_to,
                body=message_text
            )
            
            return {
                "success": True,
                "message": "Message sent successfully",
                "message_sid": message.sid
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send message: {str(e)}"
            }
