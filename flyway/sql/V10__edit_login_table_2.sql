-- Check if the column exists
SELECT COUNT(*) INTO @column_exists
FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'datadome';

-- Dynamically add the column if it does not exist
SET @sql = IF(@column_exists = 0, 'ALTER TABLE users ADD COLUMN datadome TEXT', 'SELECT "Column already exists"');

-- Execute the SQL statement
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
