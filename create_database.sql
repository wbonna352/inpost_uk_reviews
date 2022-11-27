CREATE TABLE IF NOT EXISTS reviews
(
    url TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    rate INT,
    date_of_experience DATE,
    user_url TEXT,
    user_name TEXT,
    user_reviews_count INT,
    user_location TEXT
);