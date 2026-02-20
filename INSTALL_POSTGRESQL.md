# PostgreSQL Installation Guide for Windows

## ⚠️ PostgreSQL is Required

This application requires PostgreSQL database. Here's how to install it:

## Quick Installation Steps

### Option 1: Official PostgreSQL Installer (Recommended)

1. **Download PostgreSQL:**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 13 or higher (latest stable version)
   - File size: ~200 MB

2. **Run Installer:**
   - Double-click the downloaded .exe file
   - Click "Next" through the setup wizard
   - **Important:** Remember the password you set for the postgres user!
   - Default port: 5432 (keep this)
   - Install all components (PostgreSQL Server, pgAdmin, Command Line Tools)

3. **Verify Installation:**
   ```cmd
   # Open new Command Prompt
   psql --version
   ```

4. **Create Database:**
   ```cmd
   # Connect to PostgreSQL
   psql -U postgres
   
   # Enter your password when prompted
   # Then create database:
   CREATE DATABASE tire_shop_db;
   
   # Exit
   \q
   ```d:\InventoryManagement\backend

### Option 2: Using Chocolatey (If you have it)

```powershell
choco install postgresql
```

### Option 3: Using Docker (Alternative)

```powershell
# Pull PostgreSQL image
docker pull postgres:13

# Run PostgreSQL container
docker run --name tire-shop-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=tire_shop_db -p 5432:5432 -d postgres:13
```

## After Installation

1. **Update backend/.env file:**
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tire_shop_db
   ```
   Replace `YOUR_PASSWORD` with the password you set during installation.

2. **Continue with setup:**
   - Run `python init_db.py` in backend folder
   - Start the backend server

## Troubleshooting

### PostgreSQL not in PATH
If `psql` command not found:
1. Add PostgreSQL bin folder to PATH
2. Default location: `C:\Program Files\PostgreSQL\15\bin`
3. Restart Command Prompt/PowerShell

### Connection Issues
- Check if PostgreSQL service is running (Services app)
- Verify port 5432 is not blocked by firewall
- Check username and password in .env file

## Quick Links

- **Download:** https://www.postgresql.org/download/windows/
- **Documentation:** https://www.postgresql.org/docs/
- **pgAdmin (GUI):** Installed with PostgreSQL

---

**Once PostgreSQL is installed, come back and we'll continue the setup!**
