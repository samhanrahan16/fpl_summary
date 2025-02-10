CREATE TABLE IF NOT EXISTS team_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fpl_id INT,
    fpl_code INT,
    name VARCHAR(50),
    short_name VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS audit_team_data (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,          -- ID from team_data
    fpl_id INT,
    fpl_code INT,
    name VARCHAR(50),
    short_name VARCHAR(10),
    operation_type ENUM('INSERT', 'UPDATE', 'DELETE'), -- Tracks the type of operation
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of the change
);

CREATE TRIGGER after_team_insert
AFTER INSERT ON team_data
FOR EACH ROW
BEGIN
    INSERT INTO audit_team_data (team_id, fpl_id, fpl_code, name, short_name, operation_type)
    VALUES (NEW.id, NEW.fpl_id, NEW.fpl_code, NEW.name, NEW.short_name, 'INSERT');
END;

CREATE TRIGGER after_team_update
AFTER UPDATE ON team_data
FOR EACH ROW
BEGIN
    INSERT INTO audit_team_data (team_id, fpl_id, fpl_code, name, short_name, operation_type)
    VALUES (NEW.id, NEW.fpl_id, NEW.fpl_code, NEW.name, NEW.short_name, 'UPDATE');
END;

CREATE TRIGGER after_team_delete
AFTER DELETE ON team_data
FOR EACH ROW
BEGIN
    INSERT INTO audit_team_data (team_id, fpl_id, fpl_code, name, short_name, operation_type)
    VALUES (OLD.id, OLD.fpl_id, OLD.fpl_code, OLD.name, OLD.short_name, 'DELETE');
END;

