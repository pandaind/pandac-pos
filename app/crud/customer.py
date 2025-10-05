from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.customer import Customer, LoyaltyProgram
from app.models.sale import Sale, Transaction
from app.models.employee import Payment, Employee
from app.schemas.customer import CustomerCreate, CustomerUpdate, LoyaltyProgramCreate, LoyaltyProgramUpdate
from app.schemas.customer import SaleCreate, SaleUpdate
from app.schemas.transaction import TransactionCreate, TransactionUpdate, PaymentCreate, PaymentUpdate, EmployeeCreate, EmployeeUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.name == name).first()
    
    def get_by_contact(self, db: Session, *, contact_info: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.contact_info == contact_info).first()
    
    def add_loyalty_points(self, db: Session, *, customer_id: UUID, points: int) -> Optional[Customer]:
        customer = self.get(db, id=customer_id)
        if customer:
            customer.loyalty_points += points
            db.commit()
            db.refresh(customer)
        return customer
    
    def get_purchase_history(self, db: Session, *, customer_id: UUID, days: int = 365):
        """Get purchase history for a customer"""
        from datetime import datetime, timedelta
        from app.models.pos import POSSale
        from sqlalchemy import func
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Query sales for this customer
        sales = db.query(POSSale).filter(
            POSSale.customer_id == customer_id,
            POSSale.created_at >= start_date
        ).all()
        
        if not sales:
            return None
        
        total_spent = sum(sale.total_amount or 0 for sale in sales)
        total_purchases = len(sales)
        last_purchase = max(sale.created_at for sale in sales) if sales else None
        
        return {
            "total_spent": float(total_spent),
            "total_purchases": total_purchases,
            "last_purchase_date": last_purchase
        }


class CRUDSale(CRUDBase[Sale, SaleCreate, SaleUpdate]):
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[Sale]:
        return db.query(Sale).filter(Sale.customer_id == customer_id).all()
    
    def get_sales_by_date_range(self, db: Session, *, start_date, end_date) -> List[Sale]:
        return db.query(Sale).filter(
            Sale.created_at >= start_date,
            Sale.created_at <= end_date
        ).all()
    
    def calculate_total_sales(self, db: Session, *, start_date=None, end_date=None) -> float:
        query = db.query(Sale)
        if start_date and end_date:
            query = query.filter(Sale.created_at >= start_date, Sale.created_at <= end_date)
        
        total = sum(sale.total_amount for sale in query.all())
        return total


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_by_employee(self, db: Session, *, employee_id: UUID) -> List[Transaction]:
        return db.query(Transaction).filter(Transaction.employee_id == employee_id).all()
    
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> Optional[Transaction]:
        return db.query(Transaction).filter(Transaction.sale_id == sale_id).first()


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_method(self, db: Session, *, method: str) -> List[Payment]:
        return db.query(Payment).filter(Payment.method == method).all()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Payment]:
        return db.query(Payment).filter(Payment.status == status).all()


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: UUID) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.user_id == user_id).first()
    
    def get_by_position(self, db: Session, *, position: str) -> List[Employee]:
        return db.query(Employee).filter(Employee.position == position).all()


class CRUDLoyaltyProgram(CRUDBase[LoyaltyProgram, LoyaltyProgramCreate, LoyaltyProgramUpdate]):
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> Optional[LoyaltyProgram]:
        return db.query(LoyaltyProgram).filter(LoyaltyProgram.customer_id == customer_id).first()
    
    def get_by_tier(self, db: Session, *, tier: str) -> List[LoyaltyProgram]:
        return db.query(LoyaltyProgram).filter(LoyaltyProgram.tier == tier).all()


# Create instances
customer = CRUDCustomer(Customer)
sale = CRUDSale(Sale)
transaction = CRUDTransaction(Transaction)
payment = CRUDPayment(Payment)
employee = CRUDEmployee(Employee)
loyalty_program = CRUDLoyaltyProgram(LoyaltyProgram)
