-- seed.sql

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES
('1', 'Admin', 'User', 'admin@hbnb.com', 'hashed_password', TRUE);

INSERT INTO amenities (id, name)
VALUES
('1', 'WiFi'),
('2', 'Pool'),
('3', 'Air Conditioning');