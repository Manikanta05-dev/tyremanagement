from pydantic import BaseModel
from datetime import date

class ProfitSummary(BaseModel):
    daily_profit: float
    monthly_profit: float
    total_profit: float

class SaleProfitDetail(BaseModel):
    sale_id: int
    invoice_id: str
    customer_name: str
    total_amount: float
    total_cost: float
    profit: float
    sale_date: date

class DailyClosingReport(BaseModel):
    date: date
    total_sales: float
    total_profit: float
    cash_sales: float
    upi_sales: float
    card_sales: float
    total_items_sold: int
    total_transactions: int
