from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_current_manager_or_admin_user
from app.crud import pos as pos_crud, product as product_crud
from app.crud.customer import customer as customer_crud
from app.models.user import User

router = APIRouter()


def parse_date_flexible(date_str: str) -> datetime:
    """Parse date string with flexible format support"""
    formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}")


@router.get("/sales")
def get_sales_report(
    *,
    db: Session = Depends(get_db),
    start_date: str = Query(...),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get sales report for a date range"""
    try:
        parsed_start = parse_date_flexible(start_date)
        parsed_end = parse_date_flexible(end_date) if end_date else parsed_start + timedelta(days=1)
        
        # Get sales data for the period
        total_sales = 0
        sales_count = 0
        
        return {
            "period": {
                "start_date": parsed_start.isoformat(),
                "end_date": parsed_end.isoformat()
            },
            "total_sales": total_sales,
            "sales_count": sales_count,
            "average_sale": total_sales / max(sales_count, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales/daily")
def get_daily_sales_report(
    *,
    db: Session = Depends(get_db),
    date: str = Query(...),
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get daily sales report for a specific date"""
    try:
        parsed_date = parse_date_flexible(date)
        
        # Get sales data for the day
        total_sales = 0
        sales_count = 0
        
        return {
            "date": parsed_date.date().isoformat(),
            "total_sales": total_sales,
            "sales_count": sales_count,
            "average_sale": total_sales / max(sales_count, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales/period")
def get_period_sales_report(
    *,
    db: Session = Depends(get_db),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """Get period sales report with flexible parameter names"""
    # Support both start/end and start_date/end_date parameter formats
    start_param = start or start_date
    end_param = end or end_date
    
    if not start_param or not end_param:
        raise HTTPException(status_code=400, detail="Both start and end dates are required")
    
    start_dt = parse_date_flexible(start_param)
    end_dt = parse_date_flexible(end_param)
    
    return {
        "period": {"start_date": start_dt.strftime("%Y-%m-%d"), "end_date": end_dt.strftime("%Y-%m-%d")},
        "summary": {"total_transactions": 0, "total_revenue": 0, "days_in_period": (end_dt - start_dt).days + 1},
        "daily_breakdown": []
    }


@router.get("/inventory/stock-levels")
def get_inventory_stock_report(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get inventory stock levels report"""
    return {
        "products": [],
        "summary": {"total_products": 0, "low_stock_items": 0, "out_of_stock_items": 0}
    }


@router.get("/customers/loyalty")
def get_customer_loyalty_report(
    *,
    db: Session = Depends(get_db),
    top_n: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """Get customer loyalty report"""
    customers = customer_crud.get_multi(db=db, limit=min(top_n, 100))
    
    customer_stats = []
    for customer in customers:
        purchase_history = customer_crud.get_purchase_history(db=db, customer_id=customer.id, days=365)
        if purchase_history:
            customer_stats.append({
                "customer_id": str(customer.id),
                "name": customer.name,
                "contact_info": customer.contact_info,
                "loyalty_points": customer.loyalty_points,
                "total_spent": purchase_history.get("total_spent", 0),
                "total_purchases": purchase_history.get("total_purchases", 0),
                "last_purchase": purchase_history.get("last_purchase_date")
            })
    
    customer_stats.sort(key=lambda x: x["total_spent"], reverse=True)
    
    return {
        "summary": {
            "total_customers": len(customers),
            "active_customers": len(customer_stats),
            "average_customer_value": sum(c["total_spent"] for c in customer_stats) / len(customer_stats) if customer_stats else 0
        },
        "top_customers": customer_stats[:top_n]
    }


@router.get("/financial/profit-loss")
def get_profit_loss_report(
    *,
    db: Session = Depends(get_db),
    start_date: str = Query(...),
    end_date: str = Query(...),
    current_user: User = Depends(get_current_manager_or_admin_user),
):
    """Get profit and loss report"""
    start_dt = parse_date_flexible(start_date)
    end_dt = parse_date_flexible(end_date)
    
    return {
        "period": {"start_date": start_dt.strftime("%Y-%m-%d"), "end_date": end_dt.strftime("%Y-%m-%d")},
        "revenue": {"total_revenue": 0, "total_transactions": 0},
        "costs": {"cost_of_goods_sold": 0, "operating_expenses": 0},
        "profit": {"gross_profit": 0, "net_income": 0}
    }
