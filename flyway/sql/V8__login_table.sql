CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    manager_id INT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
