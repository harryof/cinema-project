CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT,
    duration INTEGER,
    age_rating INTEGER
);

CREATE TABLE IF NOT EXISTS halls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    rows INTEGER,
    seats_in_row INTEGER
);

CREATE TABLE IF NOT EXISTS viewers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    age INTEGER
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    film_id INTEGER,
    hall_id INTEGER,
    start TEXT,
    FOREIGN KEY (film_id) REFERENCES films (id),
    FOREIGN KEY (hall_id) REFERENCES halls (id)
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    viewer_id INTEGER,
    seat INTEGER,
    cost REAL,
    FOREIGN KEY (session_id) REFERENCES sessions (id),
    FOREIGN KEY (viewer_id) REFERENCES viewers (id)
);
