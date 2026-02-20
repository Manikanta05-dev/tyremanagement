# Contributing to Tire Shop Inventory Management

First off, thank you for considering contributing to this project! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

---

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards others

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement needed?
- **Proposed solution**
- **Alternative solutions** considered

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - simple issues for beginners
- `help wanted` - issues that need attention

---

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Git

### Setup Steps

1. **Fork the repository**
```bash
# Click "Fork" on GitHub
```

2. **Clone your fork**
```bash
git clone https://github.com/YOUR-USERNAME/tire-shop-inventory.git
cd tire-shop-inventory
```

3. **Add upstream remote**
```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/tire-shop-inventory.git
```

4. **Create a branch**
```bash
git checkout -b feature/your-feature-name
```

5. **Setup backend**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
```

6. **Setup frontend**
```bash
cd frontend
npm install
```

7. **Run the application**
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## Coding Standards

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** where possible
- Write **docstrings** for functions and classes
- Keep functions small and focused
- Use meaningful variable names

**Example**:
```python
def calculate_discount(subtotal: float, discount_type: str, discount_value: float) -> float:
    """
    Calculate discount amount based on type and value.
    
    Args:
        subtotal: Total amount before discount
        discount_type: Either 'flat' or 'percent'
        discount_value: Discount amount or percentage
    
    Returns:
        Calculated discount amount
    """
    if discount_type == 'percent':
        return (subtotal * discount_value) / 100
    return discount_value
```

### JavaScript/React (Frontend)

- Use **ES6+** syntax
- Follow **Airbnb style guide**
- Use **functional components** with hooks
- Keep components small and reusable
- Use meaningful component and variable names

**Example**:
```javascript
const DiscountCalculator = ({ subtotal, discountType, discountValue }) => {
  const calculateDiscount = () => {
    if (discountType === 'percent') {
      return (subtotal * discountValue) / 100
    }
    return discountValue
  }
  
  return (
    <div className="discount-summary">
      <span>Discount: ₹{calculateDiscount().toFixed(2)}</span>
    </div>
  )
}
```

### Code Formatting

**Backend**:
```bash
# Format with black
black app/

# Sort imports
isort app/

# Lint with flake8
flake8 app/
```

**Frontend**:
```bash
# Format with prettier
npm run format

# Lint with eslint
npm run lint
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(sales): add discount calculation feature

- Implement flat and percentage discount
- Update sales schema with discount fields
- Add discount UI in sales form

Closes #123
```

```bash
fix(auth): resolve token expiry validation issue

Token validation was not checking expiry correctly,
causing expired tokens to be accepted.

Fixes #456
```

---

## Pull Request Process

### Before Submitting

1. **Update your branch**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Run tests**
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

3. **Check code quality**
```bash
# Backend
black app/
flake8 app/

# Frontend
npm run lint
```

4. **Update documentation** if needed

### Submitting PR

1. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request** on GitHub

3. **Fill out PR template**:
   - Description of changes
   - Related issue number
   - Screenshots (if UI changes)
   - Testing done
   - Checklist completed

### PR Template

```markdown
## Description
Brief description of changes

## Related Issue
Closes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Screenshots
(if applicable)

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
```

### Review Process

- At least one approval required
- All CI checks must pass
- No merge conflicts
- Code review feedback addressed

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_sales.py

# Run specific test
pytest tests/test_sales.py::test_create_sale
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- Sales.test.jsx
```

### Writing Tests

**Backend Example**:
```python
def test_calculate_discount_flat():
    """Test flat discount calculation"""
    result = calculate_discount(1000, 'flat', 100)
    assert result == 100

def test_calculate_discount_percent():
    """Test percentage discount calculation"""
    result = calculate_discount(1000, 'percent', 10)
    assert result == 100
```

**Frontend Example**:
```javascript
describe('DiscountCalculator', () => {
  it('calculates flat discount correctly', () => {
    const { getByText } = render(
      <DiscountCalculator 
        subtotal={1000} 
        discountType="flat" 
        discountValue={100} 
      />
    )
    expect(getByText('Discount: ₹100.00')).toBeInTheDocument()
  })
})
```

---

## Documentation

### Code Documentation

- Add docstrings to Python functions
- Add JSDoc comments to JavaScript functions
- Document complex logic
- Update README if adding features

### API Documentation

- Update OpenAPI/Swagger docs
- Document new endpoints
- Include request/response examples
- Document error responses

---

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Contact maintainers

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

---

Thank you for contributing! 🎉
