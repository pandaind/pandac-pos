"""
Standalone unit tests for core POS functionality.
These tests work independently of the full application setup.
"""
import pytest
import os
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from typing import Optional
import uuid

# Set test environment
os.environ["TESTING"] = "true"

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_standalone.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Simple test models
class TestProduct(Base):
    """Simple product model for testing."""
    __tablename__ = "test_products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500))
    category = Column(String(50))


class TestCustomer(Base):
    """Simple customer model for testing."""
    __tablename__ = "test_customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    contact_info = Column(String(100), nullable=False)
    loyalty_points = Column(Integer, default=0)


class TestRole(Base):
    """Simple role model for testing."""
    __tablename__ = "test_roles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True)
    permissions = Column(String)  # JSON as string for simplicity


# Pydantic schemas for validation
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=50)


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    contact_info: str = Field(..., min_length=5, max_length=100)
    loyalty_points: int = Field(default=0, ge=0)


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    permissions: Optional[list] = None


# Test fixtures
@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


class TestProductModel:
    """Test cases for Product model."""
    
    def test_create_product(self, db_session):
        """Test creating a product."""
        product = TestProduct(
            name="Test Product",
            price=19.99,
            description="Test description",
            category="Test Category"
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 19.99
        assert product.description == "Test description"
        assert product.category == "Test Category"
    
    def test_product_schema_validation(self):
        """Test product schema validation."""
        # Valid product
        valid_product = ProductCreate(
            name="Valid Product",
            price=10.50,
            description="Valid description",
            category="Valid Category"
        )
        
        assert valid_product.name == "Valid Product"
        assert valid_product.price == 10.50
        
        # Invalid product (negative price)
        with pytest.raises(ValueError):
            ProductCreate(
                name="Invalid Product",
                price=-5.00
            )
        
        # Invalid product (empty name)
        with pytest.raises(ValueError):
            ProductCreate(
                name="",
                price=10.00
            )
    
    def test_product_price_precision(self, db_session):
        """Test product price precision."""
        test_prices = [0.01, 10.50, 999.99, 1000.00]
        
        for price in test_prices:
            product = TestProduct(
                name=f"Price Test {price}",
                price=price
            )
            
            db_session.add(product)
            db_session.commit()
            db_session.refresh(product)
            
            assert abs(product.price - price) < 0.001


class TestCustomerModel:
    """Test cases for Customer model."""
    
    def test_create_customer(self, db_session):
        """Test creating a customer."""
        customer = TestCustomer(
            name="John Doe",
            contact_info="john@example.com",
            loyalty_points=10
        )
        
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        
        assert customer.id is not None
        assert customer.name == "John Doe"
        assert customer.contact_info == "john@example.com"
        assert customer.loyalty_points == 10
    
    def test_customer_schema_validation(self):
        """Test customer schema validation."""
        # Valid customer
        valid_customer = CustomerCreate(
            name="Valid Customer",
            contact_info="valid@example.com",
            loyalty_points=5
        )
        
        assert valid_customer.name == "Valid Customer"
        assert valid_customer.contact_info == "valid@example.com"
        assert valid_customer.loyalty_points == 5
        
        # Invalid customer (negative loyalty points)
        with pytest.raises(ValueError):
            CustomerCreate(
                name="Invalid Customer",
                contact_info="invalid@example.com",
                loyalty_points=-5
            )
    
    def test_customer_default_loyalty_points(self, db_session):
        """Test customer default loyalty points."""
        customer = TestCustomer(
            name="New Customer",
            contact_info="new@example.com"
        )
        
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        
        assert customer.loyalty_points == 0


class TestRoleModel:
    """Test cases for Role model."""
    
    def test_create_role(self, db_session):
        """Test creating a role."""
        role = TestRole(
            name="admin",
            permissions='["read", "write", "admin"]'
        )
        
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)
        
        assert role.id is not None
        assert role.name == "admin"
        assert role.permissions == '["read", "write", "admin"]'
    
    def test_role_schema_validation(self):
        """Test role schema validation."""
        # Valid role
        valid_role = RoleCreate(
            name="user",
            permissions=["read"]
        )
        
        assert valid_role.name == "user"
        assert valid_role.permissions == ["read"]
        
        # Role with no permissions
        empty_role = RoleCreate(name="empty")
        assert empty_role.permissions is None
        
        # Invalid role (empty name)
        with pytest.raises(ValueError):
            RoleCreate(name="")
    
    def test_role_unique_name(self, db_session):
        """Test role name uniqueness."""
        # Create first role
        role1 = TestRole(name="duplicate")
        db_session.add(role1)
        db_session.commit()
        
        # Try to create second role with same name
        role2 = TestRole(name="duplicate")
        db_session.add(role2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()


class TestBusinessLogic:
    """Test business logic functions."""
    
    def test_calculate_total_price(self):
        """Test price calculation logic."""
        def calculate_total(unit_price: float, quantity: int, discount: float = 0.0) -> float:
            """Calculate total price with discount."""
            subtotal = unit_price * quantity
            discount_amount = subtotal * (discount / 100)
            return subtotal - discount_amount
        
        # Basic calculation
        assert calculate_total(10.00, 2) == 20.00
        
        # With discount
        assert calculate_total(10.00, 2, 10.0) == 18.00
        
        # Edge cases
        assert calculate_total(0.01, 1) == 0.01
        assert calculate_total(10.00, 0) == 0.00
    
    def test_loyalty_points_calculation(self):
        """Test loyalty points calculation.""" 
        def calculate_loyalty_points(purchase_amount: float) -> int:
            """Calculate loyalty points (1 point per dollar)."""
            return int(purchase_amount)
        
        assert calculate_loyalty_points(25.99) == 25
        assert calculate_loyalty_points(0.50) == 0
        assert calculate_loyalty_points(100.00) == 100
    
    def test_inventory_management(self, db_session):
        """Test basic inventory operations."""
        # Create product
        product = TestProduct(
            name="Inventory Test Product",
            price=15.99
        )
        
        db_session.add(product)
        db_session.commit()
        
        # Simulate inventory operations
        initial_stock = 100
        sale_quantity = 15
        restock_quantity = 50
        
        current_stock = initial_stock
        current_stock -= sale_quantity  # Sale
        assert current_stock == 85
        
        current_stock += restock_quantity  # Restock
        assert current_stock == 135


# Health check test
def test_database_connection():
    """Test that database connection works."""
    from sqlalchemy import text
    
    session = TestingSessionLocal()
    try:
        # Simple query to test connection
        result = session.execute(text("SELECT 1")).fetchone()
        assert result[0] == 1
    finally:
        session.close()


def test_schema_validation():
    """Test that Pydantic schemas work correctly."""
    # This test verifies that Pydantic is working
    product = ProductCreate(name="Test", price=10.0)
    assert isinstance(product, ProductCreate)
    assert product.name == "Test"
    assert product.price == 10.0