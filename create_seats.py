import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@2003",
    database="movie_booking"
)
cursor = conn.cursor(dictionary=True)

# Get all movies
cursor.execute("SELECT id, name FROM movies")
movies = cursor.fetchall()

# Define standard theatre layout (like your reference image)
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
seats_per_row = 20

print("Creating seats for all movies...")

for movie in movies:
    movie_id = movie['id']
    movie_name = movie['name']
    
    # Check if seats already exist for this movie
    cursor.execute("SELECT COUNT(*) as count FROM seats WHERE movie_id = %s", (movie_id,))
    existing_seats = cursor.fetchone()['count']
    
    if existing_seats > 0:
        print(f"Movie '{movie_name}' already has {existing_seats} seats - skipping")
        continue
    
    print(f"Creating seats for '{movie_name}'...")
    
    # Create seats for this movie
    seats_to_insert = []
    for row in rows:
        for seat_num in range(1, seats_per_row + 1):
            seat_no = f"{row}{seat_num}"
            seats_to_insert.append((movie_id, seat_no, False))
    
    # Insert all seats for this movie
    cursor.executemany(
        "INSERT INTO seats (movie_id, seat_no, is_booked) VALUES (%s, %s, %s)",
        seats_to_insert
    )
    
    print(f"Created {len(seats_to_insert)} seats for '{movie_name}'")

conn.commit()
print("\nAll movies now have seats!")

# Verify
cursor.execute("SELECT movie_id, COUNT(*) as seat_count FROM seats GROUP BY movie_id")
results = cursor.fetchall()
print("\nSeat count per movie:")
for result in results:
    cursor.execute("SELECT name FROM movies WHERE id = %s", (result['movie_id'],))
    movie_name = cursor.fetchone()['name']
    print(f"Movie ID {result['movie_id']} ({movie_name}): {result['seat_count']} seats")

cursor.close()
conn.close()
