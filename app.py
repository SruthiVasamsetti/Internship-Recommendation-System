from flask import Flask, render_template, request, redirect, url_for, session, flash
import MySQLdb
import MySQLdb.cursors
import hashlib

app = Flask(__name__)
app.secret_key = 'internship_recommendation_system_2024'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'internship_db'
}

def get_db_connection():
    try:
        connection = MySQLdb.connect(**DB_CONFIG)
        print("Database connection successful")
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/role_selection')
def role_selection():
    return render_template('role_selection.html')

@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Check if email already exists
                check_query = "SELECT id FROM students WHERE email = %s"
                cursor.execute(check_query, (email,))
                if cursor.fetchone():
                    flash('Email already registered! Please Login.', 'error')
                    return render_template('student_register.html')
                
                query = "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, password))
                connection.commit()
                session['student_id'] = cursor.lastrowid
                session['student_name'] = name
                session['student_email'] = email
                flash('Registration successful! Welcome to your dashboard.', 'success')
                return redirect(url_for('student_dashboard'))
            except Exception as e:
                flash(f'Registration failed: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
    
    return render_template('student_register.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check student credentials against database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                query = "SELECT * FROM students WHERE email = %s"
                cursor.execute(query, (email,))
                student = cursor.fetchone()
                
                if student:
                    # For demo purposes, we'll use a simple password check
                    # In production, you should hash passwords and compare
                    if password == "password123" or password == student.get('password', ''):
                        session['student_id'] = student['id']
                        session['student_name'] = student['name']
                        session['student_email'] = student['email']
                        return redirect(url_for('student_dashboard'))
                    else:
                        flash('Incorrect Password!', 'error')
                else:
                    flash('Student not found with this email address', 'error')
            except Exception as e:
                flash(f'Login error: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Database connection error', 'error')
    
    return render_template('student_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('role_selection'))
    
    student_info = {
        'name': session.get('student_name'),
        'email': session.get('student_email'),
        'skills': session.get('student_skills')
    }
    
    return render_template('student_dashboard.html', student=student_info)

@app.route('/eligibility_form', methods=['GET', 'POST'])
def eligibility_form():
    if 'student_id' not in session:
        return redirect(url_for('role_selection'))
    
    # Fetch dynamic domains and skills for GET requests
    domains = []
    skills = []
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Fetch unique domains
            domain_query = "SELECT DISTINCT domain FROM internships WHERE domain IS NOT NULL AND domain != '' ORDER BY domain"
            cursor.execute(domain_query)
            domain_results = cursor.fetchall()
            domains = [result['domain'] for result in domain_results]
            
            # Fetch unique skills from required_skills (split and deduplicate)
            skills_query = "SELECT DISTINCT required_skills FROM internships WHERE required_skills IS NOT NULL AND required_skills != ''"
            cursor.execute(skills_query)
            skill_results = cursor.fetchall()
            
            # Split skills by comma and deduplicate
            all_skills = set()
            for result in skill_results:
                skill_list = [skill.strip() for skill in result['required_skills'].split(',')]
                all_skills.update(skill_list)
            skills = sorted(list(all_skills))
            
        except Exception as e:
            print(f"Error fetching domains and skills: {e}")
        finally:
            cursor.close()
            connection.close()
    
    if request.method == 'POST':
        cgpa = request.form['cgpa']
        skills_selected = request.form.getlist('skills')
        domain = request.form['domain']
        year = request.form['year']
        branch = request.form['branch']
        backlogs = request.form.get('backlogs')
        
        # Check if student has backlogs7u
        if backlogs == 'yes':
            return render_template('not_eligible_backlogs.html')
        
        # Store form data in session for recommendation logic
        session['eligibility_cgpa'] = cgpa
        session['eligibility_skills'] = skills_selected
        session['eligibility_domain'] = domain
        session['eligibility_year'] = year
        session['eligibility_branch'] = branch
        
        # Save eligibility data to students table
        student_id = session.get('student_id')
        if student_id:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    update_query = """UPDATE students 
                                    SET cgpa=%s, skills=%s, domain=%s, year=%s, branch=%s 
                                    WHERE id=%s"""
                    cursor.execute(update_query, (cgpa, ', '.join(skills_selected), domain, year, branch, student_id))
                    connection.commit()
                    print(f"DEBUG: Updated student {student_id} with eligibility data")
                except Exception as e:
                    print(f"Error updating student eligibility: {e}")
                finally:
                    cursor.close()
                    connection.close()
        
        return redirect(url_for('recommendation_results'))
    
    return render_template('eligibility_form.html', domains=domains, skills=skills)

@app.route('/recommendation_results')
def recommendation_results():
    if 'student_id' not in session:
        return redirect(url_for('role_selection'))
    
    cgpa = float(session.get('eligibility_cgpa', 0))
    skills = session.get('eligibility_skills', [])
    domain = session.get('eligibility_domain', '')
    year = session.get('eligibility_year', '')
    
    # Handle backward compatibility: treat '4th Year' as 'Final Year'
    if year == '4th Year':
        year = 'Final Year'
        print(f"DEBUG: Converted '4th Year' to 'Final Year' for compatibility")
    
    # Debug prints to show student input
    print(f"=== DEBUG: Student Input ===")
    print(f"CGPA: {cgpa}")
    print(f"Skills: {skills}")
    print(f"Domain: '{domain}'")
    print(f"Year: '{year}'")
    print(f"===========================")
    
    connection = get_db_connection()
    recommendations = []
    
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Build base query for CGPA and domain requirements
            base_query = """
                SELECT * FROM internships 
                WHERE min_cgpa <= %s
            """
            params = [cgpa]
            
            # Add domain filter if specified using LIKE for flexible matching
            if domain:
                base_query += " AND LOWER(domain) LIKE LOWER(%s)"
                params.append(f"%{domain}%")
            
            # Add skills filter using SQL LIKE for flexible matching
            if skills and len(skills) > 0:
                skills_conditions = []
                for skill in skills:
                    skills_conditions.append("LOWER(required_skills) LIKE LOWER(%s)")
                    params.append(f"%{skill}%")
                
                # Use OR condition for flexible matching - any skill match is acceptable
                base_query += f" AND ({' OR '.join(skills_conditions)})"
            
            print(f"SQL Query: {base_query}")
            print(f"SQL Params: {params}")
            
            cursor.execute(base_query, params)
            recommendations = cursor.fetchall()
            
            print(f"Total internships found: {len(recommendations)}")
            
            # Debug output for matched internships
            for i, internship in enumerate(recommendations[:3]):  # Show first 3
                print(f"Matched internship {i+1}: {internship.get('title', 'Unknown')} - {internship.get('required_skills', '')}")
            
            print(f"\nFinal recommendations count: {len(recommendations)}")
            
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
        finally:
            cursor.close()
            connection.close()
    
    if recommendations:
        return render_template('recommendation_results.html', recommendations=recommendations)
    else:
        return render_template('no_match.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check admin credentials against database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                # First check if username exists
                query = "SELECT * FROM admins WHERE username = %s"
                cursor.execute(query, (username,))
                admin = cursor.fetchone()
                
                if admin:
                    # Username exists, now check password
                    if password == admin['password']:
                        session['admin_logged_in'] = True
                        session['admin_id'] = admin['id']
                        session['admin_username'] = admin['username']
                        return redirect(url_for('admin_dashboard'))
                    else:
                        flash('Incorrect Password!', 'error')
                else:
                    flash('Invalid Username!', 'error')
            except Exception as e:
                flash(f'Login error: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Database connection error', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html')

@app.route('/manage_internships')
def manage_internships():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    internships = []
    
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            query = "SELECT * FROM internships"
            print(f"DEBUG: Executing query: {query}")
            cursor.execute(query)
            internships = cursor.fetchall()
            print(f"DEBUG: Found {len(internships)} internships")
            print(f"DEBUG: Internships type: {type(internships)}")
            if internships:
                for i, internship in enumerate(internships[:3]):  # Show first 3 internships
                    print(f"DEBUG: Internship {i+1}: {internship}")
                    print(f"DEBUG: Company field: {internship.get('company', 'MISSING')}")
                    print(f"DEBUG: Title field: {internship.get('title', 'MISSING')}")
        except Exception as e:
            print(f"ERROR: Error fetching internships: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('manage_internships.html', internships=internships)

@app.route('/delete_internships')
def delete_internships():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    internships = []
    
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            query = "SELECT * FROM internships"
            cursor.execute(query)
            internships = cursor.fetchall()
        except Exception as e:
            print(f"ERROR: Error fetching internships: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('delete_internships.html', internships=internships)

@app.route('/update_internships')
def update_internships():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    internships = []
    
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            query = "SELECT * FROM internships"
            cursor.execute(query)
            internships = cursor.fetchall()
        except Exception as e:
            print(f"ERROR: Error fetching internships: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('update_internships.html', internships=internships)

@app.route('/admin/delete_list')
def admin_delete_list():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    internships = []
    
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            query = "SELECT * FROM internships"
            cursor.execute(query)
            internships = cursor.fetchall()
        except Exception as e:
            print(f"ERROR: Error fetching internships: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('delete_internships.html', internships=internships)

@app.route('/admin/update_list')
def admin_update_list():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    internships = []
    
    if connection:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            query = "SELECT * FROM internships"
            cursor.execute(query)
            internships = cursor.fetchall()
        except Exception as e:
            print(f"ERROR: Error fetching internships: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('update_internships.html', internships=internships)

@app.route('/add_internship', methods=['GET', 'POST'])
def add_internship():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        domain = request.form['domain']
        min_cgpa = request.form['min_cgpa']
        required_skills = request.form['required_skills']
        duration = request.form['duration']
        stipend = request.form['stipend']
        apply_link = request.form['apply_link']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """INSERT INTO internships 
                          (title, company, domain, min_cgpa, required_skills, duration, stipend, apply_link) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (title, company, domain, min_cgpa, required_skills, duration, stipend, apply_link))
                connection.commit()
                flash('Internship added successfully!', 'success')
                return redirect(url_for('manage_internships'))
            except Exception as e:
                flash(f'Failed to add internship: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
    
    return render_template('add_internship.html')

@app.route('/edit_internship/<int:internship_id>', methods=['GET', 'POST'])
def edit_internship(internship_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        domain = request.form['domain']
        min_cgpa = request.form['min_cgpa']
        required_skills = request.form['required_skills']
        duration = request.form['duration']
        stipend = request.form['stipend']
        apply_link = request.form['apply_link']
        
        if connection:
            cursor = connection.cursor()
            try:
                query = """UPDATE internships SET 
                          title=%s, company=%s, domain=%s, min_cgpa=%s, 
                          required_skills=%s, duration=%s, stipend=%s, apply_link=%s 
                          WHERE id=%s"""
                cursor.execute(query, (title, company, domain, min_cgpa, required_skills, duration, stipend, apply_link, internship_id))
                connection.commit()
                flash('Internship updated successfully!', 'success')
                return redirect(url_for('manage_internships'))
            except Exception as e:
                flash(f'Failed to update internship: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
    else:
        # GET request - fetch internship details
        internship = None
        if connection:
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                query = "SELECT * FROM internships WHERE id = %s"
                cursor.execute(query, (internship_id,))
                internship = cursor.fetchone()
            except Exception as e:
                print(f"Error fetching internship: {e}")
            finally:
                cursor.close()
                connection.close()
        
        return render_template('edit_internship.html', internship=internship)

@app.route('/delete_internship/<int:internship_id>')
def delete_internship(internship_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = "DELETE FROM internships WHERE id = %s"
            cursor.execute(query, (internship_id,))
            connection.commit()
            flash('Internship deleted successfully!', 'success')
        except Exception as e:
            flash(f'Failed to delete internship: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return redirect(url_for('manage_internships'))

@app.route('/view_students')
def view_students():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    print("DEBUG: Attempting to connect to database...")
    connection = get_db_connection()
    student_list = []
    
    if connection:
        print("DEBUG: Database connection successful")
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT DISTINCT * FROM students')
            student_list = cursor.fetchall()
            print(f"Unique students found: {student_list}")
        except Exception as e:
            print(f"ERROR: Error fetching students: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("ERROR: Failed to connect to database")
    
    return render_template('view_students.html', students=student_list)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('role_selection'))

if __name__ == '__main__':
    app.run(debug=True)
