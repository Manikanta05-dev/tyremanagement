from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db)
):
    dashboard_service = DashboardService(db)
    return dashboard_service.get_dashboard_data()
