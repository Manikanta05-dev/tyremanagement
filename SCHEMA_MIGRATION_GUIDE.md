# Schema Migration Guide

## Problem

When the FastAPI User model is updated after initial deployment, the PostgreSQL users table retains the old schema because SQLAlchemy's `Base.metadata.create_all()` does NOT alter existing tables.

This causes INSERT queries during `POST /auth/register` to fail with 500 errors due to missing columns.

## Solution

The application automatically handles schema updates in production by:

1. Detecting production environment via `ENVIRONMENT=production` env variable
2. Dropping the users table on startup (if it exists)
3. Recreating all tables with the updated schema

## How It Works

### In `backend/app/main.py`:

```python
@app.on_event("startup")
def startup_event():
    # Check environment
    environment = os.getenv("ENVIRONMENT", "development")
    is_production = environment == "production"
    
    # Drop users table in production only
    if is_production:
        User.__table__.drop(bind=engine, checkfirst=True)
    
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
```

### In `render.yaml`:

```yaml
envVars:
  - key: ENVIRONMENT
    value: production
```

## Behavior

### Development (ENVIRONMENT != "production"):
- Tables are created if they don't exist
- Existing tables are NOT dropped
- Safe for local development

### Production (ENVIRONMENT = "production"):
- Users table is dropped on every startup
- All tables are recreated with current schema
- Ensures schema always matches the model

## Important Notes

1. **Data Loss**: This approach drops the users table, so all user data is lost on redeploy
2. **Use Case**: This is suitable for:
   - Initial development/testing phase
   - Applications without production users yet
   - When you need to iterate on schema quickly

3. **Not Recommended For**:
   - Production apps with real users
   - Applications that need to preserve user data

## Better Alternatives for Production

For production applications with real users, use proper database migrations:

### Option 1: Alembic (Recommended)

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add created_at to users"

# Apply migration
alembic upgrade head
```

### Option 2: Manual SQL Migration

```sql
-- Add missing columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR;
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'staff';
```

### Option 3: Conditional Drop

Only drop table if schema version changes:

```python
# Check schema version
schema_version = db.execute("SELECT version FROM schema_version").scalar()
if schema_version != CURRENT_VERSION:
    User.__table__.drop(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine)
    # Update version
```

## Current Status

The application is configured to drop and recreate the users table on every production deployment. This is acceptable for the current development phase but should be replaced with Alembic migrations before launching to real users.

## Next Steps

1. Deploy to Render with `ENVIRONMENT=production`
2. Verify users table is recreated with correct schema
3. Test `POST /auth/register` - should work without 500 errors
4. Before production launch: Implement Alembic migrations
