CREATE TABLE IF NOT EXISTS team_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100),
    home_rating INT,
    away_rating INT
);