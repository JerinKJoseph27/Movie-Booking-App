# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] MySQL Server 8.0+ installed and running
- [ ] pip package manager installed
- [ ] Git (if cloning from GitHub)

## Installation Steps

### 1. Clone/Download the Project
```bash
git clone <repository-url>
cd movie-booking
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
```bash
# Login to MySQL
mysql -u root -p

# Run these commands in MySQL shell:
source db_config.sql
exit;
```

### 5. Configure Application
Edit `app.py` lines 13-18:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="YOUR_USERNAME",      # Change this
    password="YOUR_PASSWORD",  # Change this
    database="movie_booking"
)
```

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## Troubleshooting

### Issue: Module not found
**Solution**: Make sure you've activated the virtual environment and installed requirements
```bash
pip install -r requirements.txt
```

### Issue: Database connection error
**Solution**: Check MySQL is running and credentials are correct
```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql
```

### Issue: Port 5000 already in use
**Solution**: Change port in app.py last line:
```python
app.run(debug=True, port=5001)
```

### Issue: No movie posters showing
**Solution**: Add image files to `static/Posters/` directory and update database

## Testing the Application

1. Visit homepage - should see movie list
2. Click "Book Tickets" - should see seat selection
3. Select seats (green available, red booked)
4. Fill in name and phone (Indian format: 10 digits)
5. Confirm booking - get booking ID
6. Download ticket - get PDF file

## Next Steps

- Add more movies via SQL or admin panel
- Customize ticket design in `create_pdf_ticket()` function
- Add movie posters to enhance UI
- Configure email notifications (future feature)

## Need Help?

- Check README.md for detailed documentation
- Review error messages in terminal
- Ensure all prerequisites are met
- Verify database tables are created correctly
