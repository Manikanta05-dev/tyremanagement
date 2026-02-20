from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List
from app.repositories.sales_repository import SalesRepository
from app.schemas.profit import ProfitSummary, SaleProfitDetail, DailyClosingReport
from app.models.sales import Sales, PaymentMode

class ProfitService:
    def __init__(self, db: Session):
        self.db = db
        self.sales_repo = SalesRepository(db)
    
    def calculate_sale_profit(self, sale) -> float:
        """Calculate profit for a single sale"""
        total_cost = 0
        for item in sale.items:
            # Get purchase price from tire inventory
            purchase_price = item.tire.purchase_price
            total_cost += purchase_price * item.quantity
        
        profit = sale.total_amount - total_cost
        return profit
    
    def get_profit_summary(self) -> ProfitSummary:
        """Get daily, monthly, and total profit"""
        today = date.today()
        now = datetime.now()
        
        # Get all sales
        all_sales = self.sales_repo.get_all(limit=10000)
        
        daily_profit = 0
        monthly_profit = 0
        total_profit = 0
        
        for sale in all_sales:
            profit = self.calculate_sale_profit(sale)
            total_profit += profit
            
            sale_date = sale.sale_date.date() if isinstance(sale.sale_date, datetime) else sale.sale_date
            
            if sale_date == today:
                daily_profit += profit
            
            if sale_date.year == now.year and sale_date.month == now.month:
                monthly_profit += profit
        
        return ProfitSummary(
            daily_profit=daily_profit,
            monthly_profit=monthly_profit,
            total_profit=total_profit
        )
    
    def get_sale_profit_details(self, skip: int = 0, limit: int = 100) -> List[SaleProfitDetail]:
        """Get profit details for each sale"""
        sales = self.sales_repo.get_all(skip, limit)
        
        profit_details = []
        for sale in sales:
            total_cost = sum(item.tire.purchase_price * item.quantity for item in sale.items)
            profit = sale.total_amount - total_cost
            
            sale_date = sale.sale_date.date() if isinstance(sale.sale_date, datetime) else sale.sale_date
            
            profit_details.append(SaleProfitDetail(
                sale_id=sale.id,
                invoice_id=sale.invoice_id,
                customer_name=sale.customer_name,
                total_amount=sale.total_amount,
                total_cost=total_cost,
                profit=profit,
                sale_date=sale_date
            ))
        
        return profit_details
    
    def get_daily_closing_report(self, report_date: date = None) -> DailyClosingReport:
        """Generate daily closing report"""
        if report_date is None:
            report_date = date.today()
        
        # Get sales for the day
        sales = self.db.query(Sales).filter(
            func.date(Sales.sale_date) == report_date
        ).all()
        
        total_sales = 0
        total_profit = 0
        cash_sales = 0
        upi_sales = 0
        card_sales = 0
        total_items_sold = 0
        
        for sale in sales:
            total_sales += sale.total_amount
            total_profit += self.calculate_sale_profit(sale)
            
            # Count by payment mode
            if sale.payment_mode == PaymentMode.CASH:
                cash_sales += sale.total_amount
            elif sale.payment_mode == PaymentMode.UPI:
                upi_sales += sale.total_amount
            elif sale.payment_mode == PaymentMode.CARD:
                card_sales += sale.total_amount
            
            # Count items
            total_items_sold += sum(item.quantity for item in sale.items)
        
        return DailyClosingReport(
            date=report_date,
            total_sales=total_sales,
            total_profit=total_profit,
            cash_sales=cash_sales,
            upi_sales=upi_sales,
            card_sales=card_sales,
            total_items_sold=total_items_sold,
            total_transactions=len(sales)
        )
