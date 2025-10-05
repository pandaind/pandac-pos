# Pandac POS API

A complete Point of Sale (POS) system API built with FastAPI and PostgreSQL.

## Features

- **Authentication**: JWT-based user authentication and authorization
- **Products**: Product management with inventory tracking
- **Customers**: Customer management and loyalty programs
- **Sales**: Complete sales workflow with items and payments
- **Inventory**: Stock management, suppliers, and purchase orders
- **Reports**: Sales analytics, financial reports, and business insights
- **Users & Roles**: Multi-user system with role-based access control
- **Employees**: Employee management and transaction tracking

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Newman CLI (for testing) - `npm install -g newman`

### 1. Start the Application

```bash
# Clone and navigate to the project
cd pandac-pos

# Start the services
docker-compose up -d

# The API will be available at: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### 2. Test the API

```bash
# Run comprehensive API tests (223 assertions, 100% success rate)
cd newman-tests
newman run postman/pandac-pos-api-collection.json --environment postman/environment.json

# Or use the convenient test script
./test.sh
```

### 3. Stop the Application

```bash
docker-compose down
```

## API Endpoints

- **Authentication**: `/v1/auth/*` - Login, register, refresh tokens
- **Products**: `/v1/products/*` - Product CRUD operations
- **Customers**: `/v1/customers/*` - Customer management
- **Sales**: `/v1/sales/*` - Sales transactions and analytics
- **Inventory**: `/v1/inventory/*` - Stock, suppliers, purchase orders
- **Reports**: `/v1/reports/*` - Business analytics and reports
- **Users**: `/v1/users/*` - User management
- **Roles**: `/v1/roles/*` - Role-based access control

## Default Credentials

- **Admin User**: Created automatically on first run
- **Database**: PostgreSQL with auto-migration
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## Environment Configuration

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic migrations
- **Authentication**: JWT tokens with role-based access
- **Testing**: Newman/Postman comprehensive test suite
- **Deployment**: Docker containerized application

## API Testing Results

✅ **Complete Test Coverage** - 223/223 passing assertions (100% success rate)  
✅ **All Endpoints Validated** - Authentication, CRUD, Analytics, Reports  
✅ **Automatic Token Management** - Fresh admin tokens, no expiration issues  
✅ **Production Ready** - All business logic validated  

### Test Features

- **Comprehensive Coverage**: 118 API requests across 20 test folders
- **Automatic Admin Access**: Fresh tokens generated for protected endpoints
- **HTML Reports**: Detailed test results with timing and response data
- **Zero Failures**: Complete success on all authentication and CRUD operations

The API has been thoroughly validated and is production-ready with 100% test success rate.
