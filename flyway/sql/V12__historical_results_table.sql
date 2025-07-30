CREATE TABLE IF NOT EXISTS historical_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    season INT,
    team_h INT,
    team_a INT,
    team_h_score INT,
    team_a_score INT,
    team_h_xg FLOAT,
    team_a_xg FLOAT
);
