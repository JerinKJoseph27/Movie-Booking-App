# Security Checklist Before Pushing to GitHub

## ⚠️ CRITICAL - Review Before Pushing

### 1. Database Credentials
- [ ] Remove hardcoded passwords from `app.py`
- [ ] Use environment variables or config file (not committed)
- [ ] Ensure `.env` is in `.gitignore`

### 2. Sensitive Information
- [ ] No API keys in code
- [ ] No email passwords
- [ ] No production database URLs
- [ ] No secret keys hardcoded

### 3. Files to Exclude
Already configured in `.gitignore`:
- `__pycache__/` - Python cache
- `.env` - Environment variables
- `*.pyc` - Compiled Python
- `.vscode/`, `.idea/` - IDE configs

### 4. Recommended Changes Before Push

**Current Issue**: `app.py` contains hardcoded password `root@2003`

**Solution Options**:

#### Option A: Environment Variables (Recommended)
```python
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'movie_booking')
)
```

Then create `.env` file (NOT committed):
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root@2003
DB_NAME=movie_booking
```

#### Option B: Placeholder Values (Simple)
Change in `app.py`:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE",  # Change this
    database="movie_booking"
)
```

### 5. Git Commands for Clean Push

```bash
# Check what will be committed
git status

# Review changes
git diff

# Add files (excluding those in .gitignore)
git add .

# Commit with meaningful message
git commit -m "Initial commit: Movie booking system"

# Push to GitHub
git push origin main
```

### 6. After Pushing

Update GitHub repository settings:
- [ ] Add repository description
- [ ] Add topics/tags (python, flask, mysql, booking-system)
- [ ] Enable issues
- [ ] Create GitHub Pages (if needed)
- [ ] Add social preview image

### 7. Optional Enhancements

- Add GitHub Actions for CI/CD
- Add code quality badges
- Create CONTRIBUTING.md
- Add CODE_OF_CONDUCT.md
- Set up GitHub Discussions

## Final Check

Before `git push`, verify:
```bash
# Make sure .env is ignored
git check-ignore .env

# Should output: .env

# Check for sensitive data
git grep -i password
git grep -i secret
git grep -i api_key
```

If you see hardcoded sensitive data, fix it before pushing!
