from flask import Flask, render_template, request, redirect, make_response, jsonify
import mysql.connector
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from io import BytesIO
import datetime

app = Flask(__name__)

# Database Configuration
# IMPORTANT: Update these credentials with your MySQL details before running
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE",  # Change this to your MySQL password
    database="movie_booking"
)
cursor = conn.cursor(dictionary=True)

def validate_name(name):
    """Validate name - only letters, spaces, dots, and hyphens allowed"""
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    name = name.strip()
    if len(name) > 50:
        return False, "Name must be less than 50 characters"
    
    # Allow letters, spaces, dots, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\.\-\']+$", name):
        return False, "Name can only contain letters, spaces, dots, hyphens, and apostrophes"
    
    return True, ""

def validate_phone(phone):
    """Validate Indian phone numbers"""
    if not phone:
        return False, "Phone number is required"
    
    # Remove all non-digit characters
    phone_digits = re.sub(r'\D', '', phone)
    
    # Check for valid Indian phone number patterns
    if len(phone_digits) == 10:
        # 10-digit mobile number
        if phone_digits[0] in ['6', '7', '8', '9']:
            return True, phone_digits
        else:
            return False, "Mobile number must start with 6, 7, 8, or 9"
    elif len(phone_digits) == 11 and phone_digits[0] == '0':
        # 11-digit number starting with 0 (STD code)
        return True, phone_digits
    elif len(phone_digits) == 12 and phone_digits[:2] == '91':
        # 12-digit number starting with 91 (country code)
        if phone_digits[2] in ['6', '7', '8', '9']:
            return True, phone_digits
        else:
            return False, "Mobile number must start with 6, 7, 8, or 9 after country code"
    else:
        return False, "Phone number must be 10 digits (mobile) or include valid STD/country code"

def generate_booking_id():
    """Generate a unique booking ID"""
    import random
    import string
    timestamp = datetime.datetime.now().strftime("%y%m%d")
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"BK{timestamp}{random_part}"

def create_pdf_ticket(booking_data):
    """Generate PDF ticket with enhanced formatting"""
    try:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Colors
        primary_color = HexColor('#1e3c72')
        accent_color = HexColor('#FFD700')
        text_color = HexColor('#2c3e50')
        white_color = HexColor('#FFFFFF')
        
        # Header background
        p.setFillColor(primary_color)
        p.rect(0, height - 120, width, 120, fill=1)
        
        # Logo/Title
        p.setFillColor(white_color)
        p.setFont("Helvetica-Bold", 28)
        p.drawString(50, height - 55, "🎬 CinemaMax")
        p.setFont("Helvetica", 14)
        p.drawString(50, height - 75, "Your Premium Cinema Experience")
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, height - 95, f"Booking ID: {booking_data['booking_id']}")
        
        # Ticket border
        p.setStrokeColor(primary_color)
        p.setLineWidth(2)
        p.rect(30, 100, width - 60, height - 220, stroke=1, fill=0)
        
        # Movie title section
        p.setFillColor(accent_color)
        p.rect(40, height - 180, width - 80, 40, fill=1)
        p.setFillColor(HexColor('#000000'))
        p.setFont("Helvetica-Bold", 18)
        movie_title = booking_data['movie_name']
        # Center the movie title
        title_width = p.stringWidth(movie_title, "Helvetica-Bold", 18)
        p.drawString((width - title_width) / 2, height - 170, movie_title)
        
        # Customer info section
        y_position = height - 220
        p.setFillColor(text_color)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, "TICKET HOLDER INFORMATION")
        
        # Draw a line under the header
        p.setStrokeColor(accent_color)
        p.setLineWidth(1)
        p.line(50, y_position - 5, width - 50, y_position - 5)
        
        y_position -= 25
        
        # Booking details in two columns
        left_column = [
            ("Customer Name:", booking_data['customer_name']),
            ("Phone Number:", booking_data['phone']),
            ("Booking Date:", booking_data['booking_date']),
            ("Show Time:", "8:30 PM"),
        ]
        
        right_column = [
            ("Seats:", ", ".join(booking_data['seats'])),
            ("Number of Tickets:", str(len(booking_data['seats']))),
            ("Total Amount:", f"₹{booking_data['total']}"),
            ("Screen:", "Screen 1"),
        ]
        
        # Draw left column
        for label, value in left_column:
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y_position, label)
            p.setFont("Helvetica", 10)
            p.drawString(160, y_position, value)
            y_position -= 20
        
        # Draw right column
        y_position = height - 245  # Reset for right column
        for label, value in right_column:
            p.setFont("Helvetica-Bold", 10)
            p.drawString(320, y_position, label)
            p.setFont("Helvetica", 10)
            p.drawString(430, y_position, value)
            y_position -= 20
        
        # Seat visual representation
        y_position -= 30
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(text_color)
        p.drawString(50, y_position, "YOUR RESERVED SEATS")
        p.setStrokeColor(accent_color)
        p.line(50, y_position - 5, width - 50, y_position - 5)
        
        y_position -= 30
        seat_x = 50
        seat_width = 45
        seat_height = 25
        
        for i, seat in enumerate(booking_data['seats']):
            # Seat rectangle
            p.setFillColor(accent_color)
            p.rect(seat_x, y_position, seat_width, seat_height, fill=1)
            
            # Seat text
            p.setFillColor(HexColor('#000000'))
            p.setFont("Helvetica-Bold", 10)
            text_width = p.stringWidth(seat, "Helvetica-Bold", 10)
            p.drawString(seat_x + (seat_width - text_width) / 2, y_position + 8, seat)
            
            seat_x += seat_width + 10
            if seat_x > width - 100:  # Wrap to next row if needed
                seat_x = 50
                y_position -= seat_height + 10
        
        # Instructions section
        y_position -= 60
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(text_color)
        p.drawString(50, y_position, "IMPORTANT INSTRUCTIONS")
        p.setStrokeColor(accent_color)
        p.line(50, y_position - 5, width - 50, y_position - 5)
        
        y_position -= 20
        instructions = [
            "• Please arrive 30 minutes before showtime",
            "• Carry a valid ID proof along with this ticket",
            "• Outside food and beverages are not allowed",
            "• Mobile phones must be switched off during the show",
            "• This ticket is non-refundable and non-transferable",
            "• Entry is subject to security check"
        ]
        
        p.setFont("Helvetica", 9)
        for instruction in instructions:
            p.drawString(50, y_position, instruction)
            y_position -= 15
        
        # QR Code placeholder
        qr_size = 60
        qr_x = width - qr_size - 50
        qr_y = y_position - 20
        p.setStrokeColor(text_color)
        p.setLineWidth(1)
        p.rect(qr_x, qr_y, qr_size, qr_size, stroke=1, fill=0)
        p.setFont("Helvetica", 8)
        p.drawCentredString(qr_x + qr_size/2, qr_y + qr_size/2 - 4, "QR CODE")
        p.drawCentredString(qr_x + qr_size/2, qr_y + qr_size/2 - 14, "FOR ENTRY")
        
        # Footer
        p.setFillColor(primary_color)
        p.rect(0, 0, width, 80, fill=1)
        p.setFillColor(white_color)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, 50, "Thank you for choosing CinemaMax!")
        p.setFont("Helvetica", 10)
        p.drawString(50, 35, "For support: contact@cinemamax.com | +91-1234567890")
        p.drawString(50, 20, "Visit us: www.cinemamax.com | Follow @CinemaMax")
        
        # Add ticket stub perforations (visual effect)
        p.setStrokeColor(HexColor('#CCCCCC'))
        p.setLineWidth(0.5)
        for i in range(0, int(width), 10):
            p.line(i, height - 120, i + 5, height - 120)
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Return a simple error PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, "Error generating ticket PDF")
        p.drawString(100, 730, f"Booking ID: {booking_data.get('booking_id', 'Unknown')}")
        p.drawString(100, 710, "Please contact support for assistance")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

def create_seats_for_movie(movie_id):
    """Create standard theatre seats for a movie if they don't exist"""
    # Check if seats already exist
    cursor.execute("SELECT COUNT(*) as count FROM seats WHERE movie_id = %s", (movie_id,))
    existing_seats = cursor.fetchone()['count']
    
    if existing_seats > 0:
        return  # Seats already exist
    
    # Create standard theatre layout
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    seats_per_row = 20
    
    seats_to_insert = []
    for row in rows:
        for seat_num in range(1, seats_per_row + 1):
            seat_no = f"{row}{seat_num}"
            seats_to_insert.append((movie_id, seat_no, False))
    
    cursor.executemany(
        "INSERT INTO seats (movie_id, seat_no, is_booked) VALUES (%s, %s, %s)",
        seats_to_insert
    )
    conn.commit()

@app.route('/')
def home():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    
    # Ensure all movies have seats
    for movie in movies:
        create_seats_for_movie(movie['id'])
    
    return render_template("home.html", movies=movies)

@app.route('/book/<int:movie_id>')
def book(movie_id):
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    
    if not movie:
        return redirect('/')
    
    # Ensure this movie has seats
    create_seats_for_movie(movie_id)

    cursor.execute("SELECT * FROM seats WHERE movie_id = %s ORDER BY seat_no", (movie_id,))
    seats = cursor.fetchall()

    return render_template("booking.html", movie=movie, seats=seats)

@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    movie_id = request.form.get('movie_id')
    selected_seats = request.form.getlist('seats')
    
    # Validation
    errors = []
    
    # Validate name
    name_valid, name_error = validate_name(name)
    if not name_valid:
        errors.append(name_error)
    
    # Validate phone
    phone_valid, phone_result = validate_phone(phone)
    if not phone_valid:
        errors.append(phone_result)
    else:
        phone = phone_result  # Use cleaned phone number
    
    # Validate seats
    if not selected_seats:
        errors.append("Please select at least one seat")
    
    # Validate movie
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    if not movie:
        errors.append("Invalid movie selection")
    
    # If there are validation errors, return to booking page with errors
    if errors:
        cursor.execute("SELECT * FROM seats WHERE movie_id = %s ORDER BY seat_no", (movie_id,))
        seats = cursor.fetchall()
        return render_template("booking.html", movie=movie, seats=seats, errors=errors, 
                             form_data={'name': name, 'phone': request.form.get('phone', '')})
    
    # Check if selected seats are still available
    for seat in selected_seats:
        cursor.execute("SELECT is_booked FROM seats WHERE movie_id = %s AND seat_no = %s", (movie_id, seat))
        seat_status = cursor.fetchone()
        if seat_status and seat_status['is_booked']:
            errors.append(f"Seat {seat} is no longer available")
    
    if errors:
        cursor.execute("SELECT * FROM seats WHERE movie_id = %s ORDER BY seat_no", (movie_id,))
        seats = cursor.fetchall()
        return render_template("booking.html", movie=movie, seats=seats, errors=errors,
                             form_data={'name': name, 'phone': request.form.get('phone', '')})
    
    total_price = len(selected_seats) * 150  # ₹150 per ticket
    booking_id = generate_booking_id()
    booking_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save booking
    cursor.execute(
        "INSERT INTO bookings (movie_id, name, phone, seats, total_price, booking_date, booking_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (movie_id, name, phone, ','.join(selected_seats), total_price, booking_date, booking_id)
    )

    # Mark seats as booked
    for seat in selected_seats:
        cursor.execute(
            "UPDATE seats SET is_booked = TRUE WHERE movie_id = %s AND seat_no = %s",
            (movie_id, seat)
        )

    conn.commit()

    return render_template("configuration.html", 
                         name=name, 
                         seats=selected_seats, 
                         total=total_price,
                         booking_id=booking_id,
                         movie_name=movie['name'],
                         booking_date=booking_date)

@app.route('/download_ticket/<booking_id>')
def download_ticket(booking_id):
    try:
        # Get booking details
        cursor.execute("""
            SELECT b.*, m.name as movie_name 
            FROM bookings b 
            JOIN movies m ON b.movie_id = m.id 
            WHERE b.booking_id = %s
        """, (booking_id,))
        
        booking = cursor.fetchone()
        if not booking:
            return "Booking not found. Please check your booking ID.", 404
        
        # Prepare booking data for PDF
        booking_data = {
            'booking_id': booking['booking_id'],
            'movie_name': booking['movie_name'],
            'customer_name': booking['name'],
            'phone': booking['phone'],
            'seats': booking['seats'].split(',') if booking['seats'] else [],
            'total': booking['total_price'],
            'booking_date': booking['booking_date'].strftime("%Y-%m-%d %H:%M") if booking['booking_date'] else datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # Generate PDF
        pdf_buffer = create_pdf_ticket(booking_data)
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="CinemaMax_Ticket_{booking_id}.pdf"'
        response.headers['Content-Length'] = len(pdf_buffer.getvalue())
        
        return response
        
    except Exception as e:
        print(f"Error downloading ticket: {e}")
        return f"Error generating ticket: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
