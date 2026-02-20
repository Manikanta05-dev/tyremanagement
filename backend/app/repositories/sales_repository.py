from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date
from app.models.sales import Sales, SalesItem

class SalesRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, sales_data: dict, items_data: List[dict]) -> Sales:
        sale = Sales(**sales_data)
        self.db.add(sale)
        self.db.flush()
        
        for item_data in items_data:
            item = SalesItem(sale_id=sale.id, **item_data)
            self.db.add(item)
        
        self.db.commit()
        self.db.refresh(sale)
        return sale
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Sales]:
        return self.db.query(Sales).order_by(Sales.sale_date.desc()).offset(skip).limit(limit).all()
    
    def get_by_id(self, sale_id: int) -> Optional[Sales]:
        return self.db.query(Sales).filter(Sales.id == sale_id).first()
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Sales]:
        return self.db.query(Sales).filter(
            Sales.sale_date >= start_date,
            Sales.sale_date <= end_date
        ).all()
    
    def get_today_sales(self) -> float:
        today = date.today()
        result = self.db.query(func.sum(Sales.total_amount)).filter(
            func.date(Sales.sale_date) == today
        ).scalar()
        return result or 0.0
    
    def get_monthly_revenue(self, year: int, month: int) -> float:
        result = self.db.query(func.sum(Sales.total_amount)).filter(
            func.extract('year', Sales.sale_date) == year,
            func.extract('month', Sales.sale_date) == month
        ).scalar()
        return result or 0.0
    
    def get_daily_sales_chart(self, days: int = 7) -> List[dict]:
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        results = self.db.query(
            func.date(Sales.sale_date).label('date'),
            func.sum(Sales.total_amount).label('amount')
        ).filter(
            Sales.sale_date >= start_date
        ).group_by(func.date(Sales.sale_date)).all()
        
        return [{"date": str(r.date), "amount": float(r.amount)} for r in results]
    
    def generate_invoice_id(self) -> str:
        today = date.today()
        prefix = f"INV{today.strftime('%Y%m%d')}"
        last_sale = self.db.query(Sales).filter(
            Sales.invoice_id.like(f"{prefix}%")
        ).order_by(Sales.id.desc()).first()
        
        if last_sale:
            last_num = int(last_sale.invoice_id[-4:])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f"{prefix}{new_num:04d}"
