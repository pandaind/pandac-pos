from typing import Optional, List
from datetime import datetime, timedelta
from uuid import UUID
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.crud.base import CRUDBase
from app.models.pos import POSSale, POSSaleItem, POSPayment, POSDiscount
from app.models.employee import Employee
from app.schemas.pos import (
    SaleCreate, SaleUpdate, SaleItemCreate, SaleItemUpdate,
    PaymentCreate, PaymentUpdate
)
from app.schemas.misc import DiscountCreate, DiscountUpdate

logger = logging.getLogger(__name__)


class CRUDPOSSale(CRUDBase[POSSale, SaleCreate, SaleUpdate]):
    def create_with_user(self, db: Session, *, obj_in: SaleCreate, user_id: UUID) -> POSSale:
        """Create sale with items."""
        try:
            # Extract items from the sale data
            items_data = obj_in.items
            logger.info(f"Creating sale with cashier_id: {obj_in.cashier_id}")
            
            # Find or create employee for the cashier
            employee = db.query(Employee).filter(Employee.user_id == obj_in.cashier_id).first()
            if not employee:
                logger.info(f"Employee not found for user_id: {obj_in.cashier_id}, creating new employee")
                # Create employee if it doesn't exist
                employee = Employee(
                    user_id=obj_in.cashier_id,
                    name="Auto-generated Employee",
                    position="Cashier"
                )
                db.add(employee)
                db.flush()  # Ensure employee ID is generated
                db.refresh(employee)  # Refresh to get the ID
                logger.info(f"Created employee with ID: {employee.id}")
            else:
                logger.info(f"Found existing employee with ID: {employee.id}")
            
            # Create the sale with only the fields that POSSale model accepts
            db_sale = POSSale(
                customer_id=obj_in.customer_id,
                cashier_id=employee.id,  # Now this will have a valid UUID
                total_amount=obj_in.total_amount,
                discount_id=None  # Can be extended later if needed
            )
            db.add(db_sale)
            db.flush()  # Get the sale ID
            logger.info(f"Created sale with ID: {db_sale.id}")
            
            # Create sale items
            for item_data in items_data:
                item_dict = item_data.model_dump(exclude={'discount_amount'})
                logger.debug(f"Creating sale item: {item_dict}")
                db_item = POSSaleItem(sale_id=db_sale.id, **item_dict)
                db.add(db_item)
            
            db.commit()
            db.refresh(db_sale)
            logger.info(f"Successfully created sale: {db_sale.id}")
            return db_sale
        except Exception as e:
            db.rollback()
            logger.error(f"Error in create_with_user: {str(e)}")
            raise e
    
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[POSSale]:
        return db.query(POSSale).filter(POSSale.customer_id == customer_id).all()
    
    def get_by_cashier(self, db: Session, *, cashier_id: UUID) -> List[POSSale]:
        return db.query(POSSale).filter(POSSale.cashier_id == cashier_id).all()
    
    def get_sales_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime
    ) -> List[POSSale]:
        return db.query(POSSale).filter(
            and_(
                POSSale.created_at >= start_date,
                POSSale.created_at <= end_date
            )
        ).all()
    
    def get_daily_sales(self, db: Session, *, date: datetime) -> List[POSSale]:
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return self.get_sales_by_date_range(
            db, start_date=start_date, end_date=end_date
        )
    
    def calculate_daily_revenue(self, db: Session, *, date: datetime) -> float:
        sales = self.get_daily_sales(db, date=date)
        return sum(sale.total_amount for sale in sales)
    
    def get_top_selling_products(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        limit: int = 10
    ) -> List[dict]:
        result = db.query(
            POSSaleItem.product_id,
            func.sum(POSSaleItem.quantity).label('total_quantity'),
            func.sum(POSSaleItem.subtotal).label('total_revenue')
        ).join(POSSale).filter(
            and_(
                POSSale.created_at >= start_date,
                POSSale.created_at <= end_date
            )
        ).group_by(POSSaleItem.product_id).order_by(
            func.sum(POSSaleItem.quantity).desc()
        ).limit(limit).all()
        
        return [
            {
                'product_id': row.product_id,
                'total_quantity': row.total_quantity,
                'total_revenue': float(row.total_revenue)
            }
            for row in result
        ]


class CRUDPOSSaleItem(CRUDBase[POSSaleItem, SaleItemCreate, SaleItemUpdate]):
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> List[POSSaleItem]:
        return db.query(POSSaleItem).filter(POSSaleItem.sale_id == sale_id).all()
    
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[POSSaleItem]:
        return db.query(POSSaleItem).filter(POSSaleItem.product_id == product_id).all()
    
    def calculate_subtotal(self, quantity: int, unit_price: float) -> float:
        return quantity * unit_price


class CRUDPOSPayment(CRUDBase[POSPayment, PaymentCreate, PaymentUpdate]):
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> List[POSPayment]:
        return db.query(POSPayment).filter(POSPayment.sale_id == sale_id).all()
    
    def get_by_method(self, db: Session, *, payment_method: str) -> List[POSPayment]:
        return db.query(POSPayment).filter(POSPayment.payment_method == payment_method).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[POSPayment]:
        return db.query(POSPayment).filter(POSPayment.status == status).all()
    
    def get_payments_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime
    ) -> List[POSPayment]:
        return db.query(POSPayment).filter(
            and_(
                POSPayment.created_at >= start_date,
                POSPayment.created_at <= end_date
            )
        ).all()


class CRUDPOSDiscount(CRUDBase[POSDiscount, DiscountCreate, DiscountUpdate]):
    def get_active_discounts(self, db: Session) -> List[POSDiscount]:
        return db.query(POSDiscount).all()
    
    def get_by_type(self, db: Session, *, discount_type: str) -> List[POSDiscount]:
        return db.query(POSDiscount).filter(POSDiscount.type == discount_type).all()
    
    def calculate_discount_amount(self, discount: POSDiscount, original_amount: float) -> float:
        if discount.type == "percentage":
            return original_amount * (discount.value / 100)
        elif discount.type == "fixed_amount":
            return min(discount.value, original_amount)
        return 0.0


# Create instances
pos_sale = CRUDPOSSale(POSSale)
pos_sale_item = CRUDPOSSaleItem(POSSaleItem)
pos_payment = CRUDPOSPayment(POSPayment)
pos_discount = CRUDPOSDiscount(POSDiscount)
