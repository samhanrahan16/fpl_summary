CREATE TABLE IF NOT EXISTS fixtures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fpl_id INT,
    gameweek INT,
    kickoff_time TIMESTAMP,
    team_h INT,
    team_a INT,
    team_a_difficulty INT,
    team_h_difficulty INT
);