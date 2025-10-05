from fastapi import APIRouter

from app.api.v1 import auth, products, customers, sales, transactions, employees, inventory, suppliers, discounts, reports, notifications, settings, users, roles, loyalty_programs, purchase_orders, payments

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(sales.router, prefix="/sales", tags=["Sales"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(purchase_orders.router, prefix="/purchase-orders", tags=["Purchase Orders"])
api_router.include_router(discounts.router, prefix="/discounts", tags=["Discounts"])
api_router.include_router(loyalty_programs.router, prefix="/loyalty-programs", tags=["Loyalty Program"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
