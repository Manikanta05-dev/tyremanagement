# Bcrypt and Passlib Compatibility Fix

## Problem

When deploying to Render with Python 3.12, the following errors occur:

```
AttributeError: module 'bcrypt' has no attribute '__about__'
ValueError: password cannot be longer than 72 bytes
```

## Root Cause

1. **Passlib 1.7.4** was designed to work with **bcrypt 3.x**
2. **Bcrypt 4.x** (latest) introduced breaking changes:
   - Removed `__about__` module attribute
   - Changed internal API structure
   - Incompatible with passlib 1.7.4

3. When `passlib[bcrypt]` is installed without pinning bcrypt version, pip installs the latest bcrypt (4.x), causing incompatibility.

## Solution

Pin both bcrypt and passlib to compatible versions in `requirements.txt`:

```txt
bcrypt==3.2.0
passlib[bcrypt]==1.7.4
```

### Why These Versions?

- **bcrypt 3.2.0**: Last stable version of bcrypt 3.x series
- **passlib 1.7.4**: Latest version of passlib (no updates since 2020)
- These versions are tested and compatible with Python 3.12

## Installation Order

The order matters! Install bcrypt BEFORE passlib:

```bash
pip install bcrypt==3.2.0
pip install passlib[bcrypt]==1.7.4
```

In `requirements.txt`, list bcrypt before passlib:

```txt
bcrypt==3.2.0          # Must come first
passlib[bcrypt]==1.7.4 # Will use already-installed bcrypt 3.2.0
```

## Verification

After installation, verify versions:

```python
import bcrypt
import passlib

print(f"bcrypt version: {bcrypt.__version__}")  # Should be 3.2.0
print(f"passlib version: {passlib.__version__}") # Should be 1.7.4
```

Test password hashing:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("test123")
print(f"Hash: {hashed}")  # Should work without errors
```

## Alternative Solutions

### Option 1: Use bcrypt directly (without passlib)

```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
```

### Option 2: Wait for passlib update

Passlib hasn't been updated since 2020. Consider switching to:
- **argon2-cffi**: Modern password hashing
- **bcrypt** directly: Simpler, no wrapper needed

## Production Deployment

For Render deployment:

1. ✅ `requirements.txt` has `bcrypt==3.2.0` listed BEFORE `passlib[bcrypt]==1.7.4`
2. ✅ Dockerfile installs dependencies in order
3. ✅ No other packages override bcrypt version

## Common Errors and Fixes

### Error: `AttributeError: module 'bcrypt' has no attribute '__about__'`

**Cause**: bcrypt 4.x installed instead of 3.x

**Fix**:
```bash
pip uninstall bcrypt
pip install bcrypt==3.2.0
```

### Error: `ValueError: password cannot be longer than 72 bytes`

**Cause**: Password not truncated before hashing

**Fix**: Already handled in `backend/app/core/security.py`:
```python
def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        password = password_bytes.decode('utf-8', errors='ignore')
    return pwd_context.hash(password)
```

## Testing

Test locally before deploying:

```bash
# Install exact versions
pip install -r backend/requirements.txt

# Test password hashing
python -c "from app.core.security import get_password_hash; print(get_password_hash('test123'))"

# Should output: $2b$12$... (60 character bcrypt hash)
```

## References

- [Passlib Issue #148](https://foss.heptapod.net/python-libs/passlib/-/issues/148) - bcrypt 4.x compatibility
- [Bcrypt Changelog](https://github.com/pyca/bcrypt/blob/main/CHANGELOG.rst) - Breaking changes in 4.0.0
- [Passlib Documentation](https://passlib.readthedocs.io/) - CryptContext usage

## Status

✅ **FIXED** - `requirements.txt` updated with compatible versions

The backend will now deploy successfully on Render with Python 3.12!
