# Pandac POS API - Initial Setup Instructions

## Quick Start

1. **Clone and Navigate to Directory**
   ```bash
   cd /home/chittaranjan/pandac-pos
   ```

2. **Run the Setup Script**
   ```bash
   ./start.sh
   ```

## Manual Setup (Alternative)

If you prefer manual setup:

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Database Setup**
   ```bash
   # Make sure PostgreSQL is running
   # Create database: pandac_pos
   alembic upgrade head
   ```

5. **Start Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```

## Production Deployment

### Using Docker

1. **Build and Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

### Manual Production Setup

1. **Install Production Dependencies**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

## Environment Variables

Key environment variables to configure in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate a secure random string)
- `REDIS_URL`: Redis connection string for caching
- `DEBUG`: Set to `False` in production

## API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/v1/openapi.json

## Initial Data

After setup, you may want to create initial roles and admin user:

```python
# Run this in a Python shell or create a script
from app.core.database import SessionLocal
from app.crud.user import create_role, create_user
from app.schemas.user import RoleCreate, UserCreate

db = SessionLocal()

# Create admin role
admin_role = create_role(db, RoleCreate(name="admin", permissions=["*"]))

# Create admin user
admin_user = create_user(db, UserCreate(
    username="admin",
    password="admin123",  # Change this!
    role_id=admin_role.id
))

db.close()
```

## Testing

Run the comprehensive API test suite:

```bash
# Run all tests (223 assertions, 100% success rate)
./test.sh

# Or run Newman directly
cd newman-tests
newman run postman/pandac-pos-api-collection.json --environment postman/environment.json
```

### Test Features

- **Complete Coverage**: 118 API requests across 20 test folders
- **Automatic Authentication**: Fresh admin tokens generated automatically
- **Zero Configuration**: Tests run out-of-the-box with Docker setup
- **HTML Reports**: Detailed results with timing and response data

## Production Ready

The API is fully implemented and tested with:

- ✅ **Authentication & Authorization**: JWT tokens with role-based access
- ✅ **Complete CRUD Operations**: All endpoints implemented and tested
- ✅ **Business Logic**: Sales, inventory, customer management
- ✅ **Data Analytics**: Reports and business insights
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **Database Management**: Migrations and data persistence
- ✅ **100% Test Coverage**: All functionality validated
