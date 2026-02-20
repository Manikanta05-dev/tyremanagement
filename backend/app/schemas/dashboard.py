from pydantic import BaseModel
from typing import List
from datetime import date

class DashboardSummary(BaseModel):
    total_sales_today: float
    total_monthly_revenue: float
    low_stock_count: int
    total_inventory_value: float
    total_items: int
    daily_profit: float = 0.0
    monthly_profit: float = 0.0

class LowStockItem(BaseModel):
    id: int
    brand: str
    tire_size: str
    quantity: int
    
    class Config:
        from_attributes = True

class SalesChartData(BaseModel):
    date: str
    amount: float

class DashboardResponse(BaseModel):
    summary: DashboardSummary
    low_stock_items: List[LowStockItem]
    sales_chart: List[SalesChartData]
