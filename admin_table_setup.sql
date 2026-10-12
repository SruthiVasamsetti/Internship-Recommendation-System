-- Admin Table Setup for Internship Recommendation System
-- Run this script to create the admin table and insert default admin user

USE internship_db;

-- Create admin table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (username: admin, password: admin123)
INSERT INTO admins (username, password) VALUES 
('admin', 'admin123')
ON DUPLICATE KEY UPDATE password = 'admin123';

-- Verify the admin table creation and data
SELECT 'Admin table created successfully' as status;
SELECT * FROM admins;
