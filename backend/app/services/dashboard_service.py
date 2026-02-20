from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.sales_repository import SalesRepository
from app.repositories.inventory_repository import InventoryRepository
from app.services.profit_service import ProfitService
from app.schemas.dashboard import DashboardResponse, DashboardSummary, LowStockItem, SalesChartData

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.sales_repo = SalesRepository(db)
        self.inventory_repo = InventoryRepository(db)
        self.profit_service = ProfitService(db)
    
    def get_dashboard_data(self) -> DashboardResponse:
        # Get summary data
        today_sales = self.sales_repo.get_today_sales()
        now = datetime.now()
        monthly_revenue = self.sales_repo.get_monthly_revenue(now.year, now.month)
        low_stock_items = self.inventory_repo.get_low_stock(threshold=5)
        total_inventory_value = self.inventory_repo.get_total_inventory_value()
        total_items = len(self.inventory_repo.get_all(limit=10000))
        
        # Get profit data
        profit_summary = self.profit_service.get_profit_summary()
        
        summary = DashboardSummary(
            total_sales_today=today_sales,
            total_monthly_revenue=monthly_revenue,
            low_stock_count=len(low_stock_items),
            total_inventory_value=total_inventory_value,
            total_items=total_items,
            daily_profit=profit_summary.daily_profit,
            monthly_profit=profit_summary.monthly_profit
        )
        
        # Get low stock items
        low_stock = [
            LowStockItem(
                id=item.id,
                brand=item.brand,
                tire_size=item.tire_size,
                quantity=item.quantity
            )
            for item in low_stock_items
        ]
        
        # Get sales chart data
        chart_data_raw = self.sales_repo.get_daily_sales_chart(days=7)
        sales_chart = [SalesChartData(**data) for data in chart_data_raw]
        
        return DashboardResponse(
            summary=summary,
            low_stock_items=low_stock,
            sales_chart=sales_chart
        )
