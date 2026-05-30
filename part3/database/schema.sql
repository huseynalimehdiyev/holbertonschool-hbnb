-- schema.sql

CREATE TABLE users (
    id VARCHAR(60) PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE places (
    id VARCHAR(60) PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id VARCHAR(60),
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE reviews (
    id VARCHAR(60) PRIMARY KEY,
    text TEXT NOT NULL,
    rating FLOAT NOT NULL,
    user_id VARCHAR(60),
    place_id VARCHAR(60),
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

CREATE TABLE amenities (
    id VARCHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);

-- Many-to-many table (Place ↔ Amenity)
CREATE TABLE place_amenity (
    place_id VARCHAR(60),
    amenity_id VARCHAR(60),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);