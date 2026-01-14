# 🎬 CinemaMax - Movie Booking System

A comprehensive web-based movie ticket booking system built with Flask and MySQL, featuring real-time seat selection, customer validation, and automated PDF ticket generation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

CinemaMax is a modern, user-friendly movie ticket booking platform that streamlines the entire booking process. From browsing available movies to generating downloadable PDF tickets, the system provides a complete end-to-end solution for cinema operations.

### How It Works

1. **Browse Movies**: Users view a curated list of currently showing movies with posters
2. **Select Seats**: Interactive seat map shows available and booked seats in real-time
3. **Enter Details**: Validated customer information form ensures data integrity
4. **Confirm Booking**: System generates unique booking ID and reserves seats
5. **Download Ticket**: Professional PDF ticket with all booking details and QR code placeholder

## ✨ Features

### Core Functionality
- 🎥 **Multi-Movie Management** - Support for multiple movies with individual seat layouts
- 💺 **Real-Time Seat Selection** - Visual seat map with instant availability updates
- 📝 **Smart Validation** - Comprehensive validation for names and Indian phone numbers
- 🎫 **PDF Ticket Generation** - Professional, branded tickets with ReportLab
- 🔒 **Booking ID System** - Unique, timestamped booking identifiers
- 📊 **Theatre Layout** - Configurable seating (14 rows × 20 seats per screen)

### User Experience
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🎨 **Modern UI** - Gradient backgrounds, smooth animations, and professional styling
- ⚡ **Real-Time Feedback** - Instant validation messages and booking confirmations
- 🖨️ **Downloadable Tickets** - One-click PDF download with all details

### Technical Features
- ✅ **Input Validation** - Server-side validation for security
- 🔄 **Auto Seat Generation** - Automatic theatre layout creation for new movies
- 💾 **Persistent Storage** - MySQL database for reliable data management
- 🎯 **Price Calculation** - Dynamic pricing based on selected seats (₹150/seat)

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0+** - Lightweight WSGI web application framework
- **MySQL Connector** - Database connectivity and operations
- **ReportLab** - PDF generation library for tickets

### Frontend
- **HTML5** - Semantic markup structure
- **CSS3** - Modern styling with gradients and animations
- **Vanilla JavaScript** - Interactive seat selection and form handling

### Database
- **MySQL 8.0+** - Relational database management system

### Libraries & Tools
- **mysql-connector-python** - MySQL database adapter for Python
- **reportlab** - PDF generation toolkit
- **datetime** - Timestamp generation for bookings
- **re (regex)** - Pattern matching for validation

## 🏗️ System Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (Frontend)    │
└────────┬────────┘
         │ HTTP Requests
         ▼
┌─────────────────┐
│  Flask Server   │
│   (Backend)     │
│  - Routing      │
│  - Validation   │
│  - PDF Gen      │
└────────┬────────┘
         │ SQL Queries
         ▼
┌─────────────────┐
│  MySQL Database │
│  - Movies       │
│  - Seats        │
│  - Bookings     │
└─────────────────┘
```

### Data Flow

1. **User Request** → Flask routes handle incoming requests
2. **Validation** → Input sanitization and business logic checks
3. **Database Operations** → CRUD operations via MySQL connector
4. **Response Generation** → HTML templates or PDF documents
5. **Client Response** → Rendered pages or downloadable files

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/movie-booking.git
cd movie-booking
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Create database and tables
source db_config.sql

# Or manually run the SQL commands from db_config.sql
```

### Step 4: Configure Database Credentials

Edit `app.py` (lines 13-18) with your MySQL credentials:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",      # Change this
    password="your_password",  # Change this
    database="movie_booking"
)
```

### Step 5: Add Movie Posters (Optional)

Place movie poster images in the `static/Posters/` directory. Update the database with correct poster paths.

### Step 6: Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your web browser.

## ⚙️ Configuration

### Database Configuration

The database schema includes three main tables:

```sql
- movies (id, name, poster_url)
- seats (id, movie_id, seat_no, is_booked)
- bookings (id, movie_id, name, phone, seats, total_price, booking_date, booking_id)
```

### Seat Layout Configuration

Default configuration (modifiable in `create_seats_for_movie()` function):
- **Rows**: A-N (14 rows)
- **Seats per row**: 20
- **Total capacity**: 280 seats per screen

### Pricing Configuration

Current pricing (line 352 in app.py):
```python
total_price = len(selected_seats) * 150  # ₹150 per ticket
```

Modify the multiplier to change ticket prices.

## 🚀 Usage

### For End Users

1. **Browse Movies**: Navigate to the home page to see available movies
2. **Select Movie**: Click "Book Tickets" on your chosen movie
3. **Choose Seats**: Click on available seats (green) to select
4. **Fill Details**: Enter your name and phone number
5. **Confirm Booking**: Review and confirm your booking
6. **Download Ticket**: Click the download button to get your PDF ticket

### For Administrators

#### Adding New Movies

```sql
INSERT INTO movies (name, poster_url)
VALUES ('Movie Name', 'static/Posters/movie_poster.jpg');
```

The system will automatically generate seats for new movies.

#### Viewing Bookings

```sql
SELECT b.booking_id, m.name, b.name, b.phone, b.seats, b.total_price
FROM bookings b
JOIN movies m ON b.movie_id = m.id
ORDER BY b.booking_date DESC;
```

#### Resetting Seats (for testing)

```sql
UPDATE seats SET is_booked = FALSE WHERE movie_id = 1;
DELETE FROM bookings WHERE movie_id = 1;
```

## 📁 Project Structure

```
movie-booking/
│
├── app.py                      # Main Flask application
├── app_debug.py               # Debug version with additional logging
├── create_seats.py            # Utility script for seat generation
├── db_config.sql              # Database schema and initial data
├── test_validation.py         # Validation testing script
├── debug_clean.py            # Database cleanup utility
├── debug_poster.py           # Poster management utility
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation (this file)
│
├── static/                   # Static assets
│   └── Posters/             # Movie poster images
│
├── templates/               # HTML templates
│   ├── home.html           # Movie listing page
│   ├── booking.html        # Seat selection page
│   └── configuration.html  # Booking confirmation page
│
└── __pycache__/            # Python bytecode cache (gitignored)
```

## 🖼️ Screenshots

### Home Page
Movie listing with poster grid and modern UI

### Booking Page
Interactive seat selection with real-time availability

### Confirmation Page
Booking summary with downloadable PDF ticket

### PDF Ticket
Professional ticket with QR code placeholder and branding

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Display all available movies |
| GET | `/book/<movie_id>` | Show seat selection for specific movie |
| POST | `/confirm` | Process booking and reserve seats |
| GET | `/download_ticket/<booking_id>` | Generate and download PDF ticket |

## 🗄️ Database Schema

### Movies Table
```sql
CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    poster_url VARCHAR(255)
);
```

### Seats Table
```sql
CREATE TABLE seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    seat_no VARCHAR(10),
    is_booked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    name VARCHAR(100),
    phone VARCHAR(20),
    seats TEXT,
    total_price INT,
    booking_date DATETIME,
    booking_id VARCHAR(50),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test thoroughly before submitting PR
- Update documentation for new features

## 👥 Author

**Jerin K Joseph**
- GitHub: [@JerinKJoseph27](https://github.com/JerinKJoseph27)

## 🙏 Acknowledgments

- Flask documentation and community
- ReportLab for PDF generation
- MySQL for reliable data storage
- All contributors and users

## 📞 Support

For support, email bladegaming727@gmail.com or open an issue in the GitHub repository.

---

**Note**: This is a demonstration project for educational purposes. For production deployment, implement additional security measures such as:
- Environment variables for sensitive data
- HTTPS encryption
- Rate limiting
- CSRF protection
- SQL injection prevention (use parameterized queries)
- Session management
- Payment gateway integration
