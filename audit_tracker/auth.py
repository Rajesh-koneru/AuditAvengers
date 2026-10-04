from flask import Flask, redirect, render_template, Blueprint, request, jsonify, session, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import time
from datetime import datetime, timedelta
from audit_tracker.config import get_connection
from audit_tracker.test import only_one

# Securely store admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'Admin@raghu')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Raghu@1234')

# Auth blueprint
auth = Blueprint('auth', __name__)

# Flask-Login setup
login_manager = LoginManager()

# User Model for Admin and Auditors
class Users(UserMixin):
    def __init__(self, user_id, password, role):
        self.id = str(user_id)
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None

    if user_id == ADMIN_USERNAME:
        return Users(user_id=ADMIN_USERNAME, password=ADMIN_PASSWORD, role='admin')
    try:
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute('SELECT auditor_id, auditor_name FROM audit_report WHERE auditor_name=%s OR auditor_id=%s', (user_id, user_id))
            login_details = pointer.fetchone()

            if not login_details:
                pointer.execute('SELECT Auditor_id as auditor_id, Auditor_name as auditor_name FROM auditor_details WHERE Auditor_name=%s OR Auditor_id=%s', (user_id, user_id))
                login_details = pointer.fetchone()

        if login_details:
            return Users(user_id=login_details["auditor_name"], password=login_details['auditor_id'], role='auditor')
    except Exception as e:
        print(f"Database Error in user_loader: {e}")
    return None

# Login route
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form.to_dict()
        print(data)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            if request.is_json:
                return jsonify({'error': 'Please enter both username and password.'}), 400
            flash('Please enter both username and password.', 'error')
            return redirect('/login_page')

        # Check Admin Login
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.permanent = True
            user = Users(user_id=ADMIN_USERNAME, password=generate_password_hash(ADMIN_PASSWORD), role='admin')
            session['username'] = username
            session['islogin'] = 'True'
            session['role'] = 'admin'
            login_user(user)
            if request.is_json:
                return jsonify({'message': 'Login successful', 'redirect': '/admin/dashboard', 'role': 'admin'}), 200
            return redirect('/admin/dashboard')

        # Check Auditor Login from DB
        try:
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute('SELECT Auditor_id, Auditor_name, email, password FROM auditor_details WHERE Auditor_name=%s OR Auditor_id=%s OR email=%s', (username, username, username))
                auditor_data = pointer.fetchone()

                if not auditor_data:
                    pointer.execute('SELECT Auditor_id as auditor_id, Auditor_name as auditor_name, email, password FROM auditor_details WHERE Auditor_name=%s OR Auditor_id=%s OR email=%s', (username, username, username))
                    auditor_data = pointer.fetchone()

            if auditor_data:
                stored_pwd = auditor_data.get('password')
                valid_pass = False
                if stored_pwd:
                    if stored_pwd.startswith('pbkdf2:') or stored_pwd.startswith('scrypt:'):
                        valid_pass = check_password_hash(stored_pwd, password)
                    else:
                        valid_pass = (password == stored_pwd)
                if not valid_pass:
                    # Fallback for legacy database entries where password defaults to auditor_id
                    valid_pass = (password == auditor_data['Auditor_id'])

                if valid_pass:
                    user1 = Users(user_id=auditor_data['Auditor_name'], password=generate_password_hash(password), role='auditor')
                    session.permanent = True
                    session['username'] = auditor_data['Auditor_name']
                    session['islogin'] = 'True'
                    session['role'] = 'auditor'
                    session['id'] = auditor_data['Auditor_id']
                    login_user(user1)

                    target_url = f'/auditor_page/{auditor_data["Auditor_name"]}'
                    if request.is_json:
                        return jsonify({'message': 'Login successful', 'redirect': target_url, 'role': 'auditor'}), 200
                    return redirect(target_url)
                else:
                    msg = 'Invalid password. Please check your credentials.'
                    if request.is_json:
                        return jsonify({'error': msg}), 401
                    flash(msg, 'error')
                    return redirect('/login_page')
            else:
                msg = 'User not found. Please check your username or register for an account.'
                if request.is_json:
                    return jsonify({'error': msg}), 404
                flash(msg, 'error')
                return redirect('/login_page')
        except Exception as e:
            print(f"Login DB Error: {e}")
            msg = 'Database authentication error. Please try again later.'
            if request.is_json:
                return jsonify({'error': msg}), 500
            flash(msg, 'error')

    return redirect('/login_page')

# Signup / Registration route (Handles /signup, /register, and /registration endpoints)
@auth.route('/signup', methods=['POST', 'GET'])
@auth.route('/register', methods=['POST', 'GET'])
@auth.route('/registration', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        name = data.get('auditor_name') or data.get('name') or data.get('username', '').strip()
        email = data.get('email', '').strip()
        phone = str(data.get('phone') or data.get('contact', '')).strip()
        password = data.get('password', '').strip() or 'Auditor123'
        confirm_password = data.get('confirm_password') or data.get('confirmPassword', '').strip() or password

        # Validation checks
        if not name or not email or not phone:
            msg = 'All required fields (Name, Email, Phone) must be provided.'
            if request.is_json:
                return jsonify({'error': msg}), 400
            flash(msg, 'error')
            return redirect('/signup_page')

        if password != confirm_password:
            msg = 'Passwords do not match. Please verify your password.'
            if request.is_json:
                return jsonify({'error': msg}), 400
            flash(msg, 'error')
            return redirect('/signup_page')

        if '@' not in email or '.' not in email:
            msg = 'Please enter a valid email address.'
            if request.is_json:
                return jsonify({'error': msg}), 400
            flash(msg, 'error')
            return redirect('/signup_page')

        try:
            # Check if user/email already exists
            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                pointer.execute('SELECT Auditor_id FROM auditor_details WHERE Auditor_name=%s OR email=%s', (name, email))
                existing = pointer.fetchone()

            if existing:
                msg = 'An account with this Name or Email already exists. Please Sign In instead.'
                if request.is_json:
                    return jsonify({'error': msg}), 400
                flash(msg, 'error')
                return redirect('/signup_page')

            from audit_tracker.apply import generate_auditor_id
            new_auditor_id = generate_auditor_id()
            hashed_pwd = generate_password_hash(password)
            audit_id = f"AA{int(time.time()) % 10000:04d}"
            digits_only = re.sub(r'\D', '', phone)
            clean_phone = int(digits_only) if digits_only else 0

            with get_connection() as conn:
                pointer = conn.cursor(dictionary=True)
                # 1. Insert into auditor_details
                pointer.execute("""
                    INSERT INTO auditor_details (Auditor_id, Auditor_name, contact, email, password)
                    VALUES (%s, %s, %s, %s, %s)
                """, (new_auditor_id, name, clean_phone, email, hashed_pwd))

                # 2. Insert into audit_report
                pointer.execute("""
                    INSERT INTO audit_report (
                        Audit_id, auditor_id, planned_date, State, Client_id,
                        Contact, Audit_status, payment_amount, payment_status,
                        auditor_name, audit_type, location, email
                    ) VALUES (%s, %s, NOW(), 'Active', 'REG', %s, 'Pending', 0, 'Unpaid', %s, 'Auditor', 'N/A', %s)
                """, (audit_id, new_auditor_id, phone, name, email))

            success_msg = f'Registration successful! Your Auditor ID is {new_auditor_id}. Please log in.'
            if request.is_json:
                return jsonify({'message': success_msg, 'auditor_id': new_auditor_id, 'audit_id': audit_id}), 200
            flash(success_msg, 'success')
            return redirect('/login_page')

        except Exception as e:
            print(f"Signup Database Error: {e}")
            msg = 'Registration failed due to a server error. Please try again later.'
            if request.is_json:
                return jsonify({'error': msg}), 500
            flash(msg, 'error')
            return redirect('/signup_page')

    return redirect('/signup_page')

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/')

# Admin dashboard redirect route
@auth.route('/admin1')
@login_required
@only_one('admin')
def admin():
    return redirect('/admin/dashboard')

# Auditor page route
@auth.route('/auditor_page/<username>')
@login_required
def auditor(username):
    if session.get('role') == 'auditor':
        return render_template('auditor_page.html', username=session.get('username'), id=session.get('id'))
    return 'Unauthorized', 403

@auth.route('/user/home_page', methods=['GET'])
def user_home_status():
    status = session.get('islogin')
    role = session.get('role')
    if status == 'True':
        return jsonify({'status': 'logged_in', 'role': role, 'username': session.get('username')})
    else:
        return jsonify({'status': 'not_logged_in'})
