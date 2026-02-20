from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.profit import ProfitSummary, SaleProfitDetail, DailyClosingReport
from app.services.profit_service import ProfitService
from app.models.user import User

router = APIRouter(prefix="/profit", tags=["Profit"])

@router.get("/summary", response_model=ProfitSummary)
def get_profit_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profit_service = ProfitService(db)
    return profit_service.get_profit_summary()

@router.get("/details", response_model=List[SaleProfitDetail])
def get_profit_details(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profit_service = ProfitService(db)
    return profit_service.get_sale_profit_details(skip, limit)

@router.get("/daily-closing", response_model=DailyClosingReport)
def get_daily_closing_report(
    report_date: date = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profit_service = ProfitService(db)
    return profit_service.get_daily_closing_report(report_date)
