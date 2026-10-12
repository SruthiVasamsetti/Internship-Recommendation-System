# Internship Recommendation System

A Python Flask web application that helps students find suitable internships based on their skills, CGPA, and preferences. The system features role-based access for students and administrators, with a modern Bootstrap UI.

## Features

### Student Module
- **Registration**: Students can register with their details and skills
- **Dashboard**: View profile and check eligibility for internships
- **Eligibility Form**: Input CGPA, skills, domain, year, and branch
- **Recommendation System**: Get matched internships based on profile
- **No Match Handling**: Friendly message when no internships match

### Admin Module
- **Login**: Secure admin access (default: admin/admin123)
- **Dashboard**: Overview of system statistics
- **Manage Internships**: View, edit, and delete existing internships
- **Add Internships**: Create new internship opportunities
- **Full CRUD Operations**: Complete internship management

## Technical Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: Bootstrap 5
- **Styling**: Custom CSS with gradients and modern design
- **Authentication**: Session-based authentication

## Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- pip package manager

### Setup Instructions

1. **Clone/Download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - Start MySQL server
   - Run the database setup script:
     ```bash
     mysql -u root -p < database_setup.sql
     ```
   - This will create the `internship_db` database with sample data

4. **Configure database connection:**
   - Edit the `DB_CONFIG` in `app.py` if your MySQL credentials differ:
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'user': 'root',
         'password': 'your_password',
         'database': 'internship_db'
     }
     ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   - Open your browser and go to `http://localhost:5000`

## Usage

### For Students
1. Click "Get Started" on the home page
2. Select "I'm a Student"
3. Register with your details
4. Access your dashboard
5. Click "Check Eligibility" and fill the form
6. View recommended internships or "No Match" message

### For Administrators
1. Click "Get Started" on the home page
2. Select "I'm an Admin"
3. Login with credentials (admin/admin123)
4. Use the dashboard to manage internships
5. Add, edit, or delete internship listings

## Database Schema

### Students Table
- `id`: Primary key
- `name`: Student full name
- `email`: Unique email address
- `year`: Current academic year
- `skills`: Comma-separated list of skills
- `created_at`: Registration timestamp

### Internships Table
- `id`: Primary key
- `title`: Internship position title
- `company`: Company name
- `domain`: Internship domain/field
- `min_cgpa`: Minimum CGPA requirement
- `required_skills`: Required skills (comma-separated)
- `duration`: Internship duration
- `stipend`: Stipend details
- `apply_link`: Application URL
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Recommendation Logic

The system matches students with internships based on:
1. **CGPA Requirement**: Student's CGPA must meet or exceed minimum requirement
2. **Domain Match**: Student's preferred domain must match internship domain
3. **Skills Matching**: Student must have at least one required skill

## File Structure

```
INT REC PRJ/
|-- app.py                 # Main Flask application
|-- requirements.txt       # Python dependencies
|-- database_setup.sql     # Database setup script
|-- README.md             # This file
|-- templates/            # HTML templates
|   |-- home.html
|   |-- role_selection.html
|   |-- student_register.html
|   |-- student_dashboard.html
|   |-- eligibility_form.html
|   |-- recommendation_results.html
|   |-- no_match.html
|   |-- admin_login.html
|   |-- admin_dashboard.html
|   |-- manage_internships.html
|   |-- add_internship.html
|   |-- edit_internship.html
```

## Default Credentials

- **Admin Login**: admin / admin123
- **Database**: MySQL root user (no password by default)

## Customization

### Adding New Skills
Edit the skills checkboxes in `student_register.html` and `eligibility_form.html` templates.

### Modifying Recommendation Logic
Update the matching algorithm in the `recommendation_results()` function in `app.py`.

### Changing UI Theme
Modify the CSS gradients and colors in the HTML templates.

## Troubleshooting

### Database Connection Issues
- Ensure MySQL server is running
- Check database credentials in `DB_CONFIG`
- Verify the `internship_db` database exists

### Import Errors
- Install all required packages: `pip install -r requirements.txt`
- Check Python version compatibility

### Template Not Found Errors
- Ensure all HTML files are in the `templates/` folder
- Check template names match the Flask route calls

## Future Enhancements

- Email notifications for new internships
- Student application tracking
- Advanced filtering and search
- Company registration system
- Interview scheduling
- Performance analytics
- Mobile-responsive improvements

## License

This project is for educational purposes. Feel free to modify and distribute as needed.
