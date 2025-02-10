-- Change team_name to team_id and set its type to INT NOT NULL
ALTER TABLE team_ratings
CHANGE COLUMN team_name team_id INT NOT NULL;

-- Add the foreign key constraint
ALTER TABLE team_ratings
ADD CONSTRAINT fk_team_id
FOREIGN KEY (team_id) REFERENCES team_data(id);
