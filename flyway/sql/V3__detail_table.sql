CREATE TABLE IF NOT EXISTS fpl_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    detail_type VARCHAR(100),
    fpl_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_version INT,
    is_current_record BOOLEAN
);