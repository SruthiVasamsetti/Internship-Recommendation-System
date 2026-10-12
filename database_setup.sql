-- Internship Recommendation System Database Setup
-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS internship_db;
USE internship_db;

-- Drop existing tables if they exist (for fresh setup)
DROP TABLE IF EXISTS internships;
DROP TABLE IF EXISTS students;

-- Create students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    year VARCHAR(50) NOT NULL,
    branch VARCHAR(100),
    cgpa DECIMAL(3,2) DEFAULT 0.0,
    skills TEXT,
    domain VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create internships table
CREATE TABLE internships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    min_cgpa DECIMAL(3,2) DEFAULT 0.0,
    required_skills TEXT,
    duration VARCHAR(100) NOT NULL,
    stipend VARCHAR(100) NOT NULL,
    apply_link TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample internship data
INSERT INTO internships (title, company, domain, min_cgpa, required_skills, duration, stipend, apply_link) VALUES
('Software Development Intern', 'Tech Solutions Inc.', 'Software Development', 7.5, 'Python, JavaScript, SQL, Git', '3 months', 'Rs. 15,000/month', 'https://techsolutions.com/careers/internship-1'),
('Frontend Developer Intern', 'WebCraft Agency', 'Web Development', 7.0, 'HTML, CSS, JavaScript, React', '2 months', 'Rs. 12,000/month', 'https://webcraft.com/internships/frontend'),
('Data Science Intern', 'Analytics Pro', 'Data Science', 8.0, 'Python, Machine Learning, Statistics, SQL', '6 months', 'Rs. 20,000/month', 'https://analyticspro.com/data-science-intern'),
('Mobile App Developer', 'AppMasters', 'Mobile Development', 7.5, 'Java, Android Studio, Kotlin, iOS', '4 months', 'Rs. 18,000/month', 'https://appmasters.com/mobile-internship'),
('Cloud Computing Intern', 'CloudTech Systems', 'Cloud Computing', 7.0, 'AWS, Docker, Kubernetes, Linux', '3 months', 'Rs. 16,000/month', 'https://cloudtech.com/cloud-internship'),
('DevOps Engineer Intern', 'DevOps Solutions', 'DevOps', 7.5, 'Jenkins, Docker, Kubernetes, CI/CD', '3 months', 'Rs. 17,000/month', 'https://devopssolutions.com/devops-intern'),
('Cybersecurity Analyst Intern', 'SecureNet', 'Cybersecurity', 8.0, 'Network Security, Python, Ethical Hacking, Firewalls', '6 months', 'Rs. 22,000/month', 'https://securenet.com/cybersecurity-intern'),
('UI/UX Designer Intern', 'Design Studio', 'UI/UX Design', 6.5, 'Figma, Adobe XD, Photoshop, User Research', '2 months', 'Rs. 10,000/month', 'https://designstudio.com/ux-internship'),
('Machine Learning Engineer Intern', 'AI Innovations', 'Machine Learning', 8.5, 'Python, TensorFlow, PyTorch, Deep Learning', '6 months', 'Rs. 25,000/month', 'https://aiinnovations.com/ml-internship'),
('Full Stack Developer Intern', 'StartupHub', 'Software Development', 7.0, 'Node.js, React, MongoDB, Express.js', '4 months', 'Rs. 14,000/month', 'https://startuphub.com/fullstack-internship'),
('Backend Developer Intern', 'API Solutions', 'Software Development', 7.5, 'Java, Spring Boot, MySQL, REST APIs', '3 months', 'Rs. 16,000/month', 'https://apisolutions.com/backend-internship'),
('Digital Marketing Intern', 'Marketing Pro', 'Digital Marketing', 6.0, 'SEO, Social Media, Content Writing, Analytics', '2 months', 'Rs. 8,000/month', 'https://marketingpro.com/digital-marketing-internship');

-- Insert sample student data
INSERT INTO students (name, email, year, skills) VALUES
('John Smith', 'john.smith@email.com', '3rd Year', 'Python, JavaScript, SQL, React'),
('Sarah Johnson', 'sarah.johnson@email.com', '2nd Year', 'HTML, CSS, JavaScript, UI/UX Design'),
('Mike Wilson', 'mike.wilson@email.com', '4th Year', 'Java, C++, Python, Machine Learning'),
('Emily Davis', 'emily.davis@email.com', '3rd Year', 'Python, Data Science, Statistics, SQL'),
('Alex Brown', 'alex.brown@email.com', '2nd Year', 'JavaScript, React, Node.js, MongoDB'),
('Lisa Anderson', 'lisa.anderson@email.com', 'Final Year', 'AWS, Docker, Kubernetes, DevOps'),
('David Miller', 'david.miller@email.com', '3rd Year', 'Python, TensorFlow, Machine Learning, Deep Learning'),
('Jennifer Taylor', 'jennifer.taylor@email.com', '4th Year', 'Java, Spring Boot, MySQL, REST APIs'),
('Robert Garcia', 'robert.garcia@email.com', '2nd Year', 'Figma, Adobe XD, Photoshop, User Research'),
('Maria Martinez', 'maria.martinez@email.com', '3rd Year', 'SEO, Social Media, Content Writing, Analytics');

-- Show the created tables
SHOW TABLES;

-- Show sample data
SELECT 'Internships:' as table_name;
SELECT * FROM internships LIMIT 5;

SELECT 'Students:' as table_name;
SELECT * FROM students LIMIT 5;
