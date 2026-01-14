CREATE DATABASE movie_booking;

USE movie_booking;

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    poster_url VARCHAR(255)
);

CREATE TABLE seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    seat_no VARCHAR(10),
    is_booked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    name VARCHAR(100),
    phone VARCHAR(20),
    seats TEXT,
    total_price INT,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

INSERT INTO movies (name, poster_url)
VALUES ('Interstellar', 'static/posters/movie1.jpg');

INSERT INTO seats (movie_id, seat_no) VALUES
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
(1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5');
