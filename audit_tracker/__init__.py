from flask import Flask, render_template, jsonify, redirect
import os
from flask_login import login_required
from flask_session import Session
from datetime import timedelta


from audit_tracker.mail_config import mail

# create app is the function for the app audit avengers where everything runs through this function
def create_App():
    from audit_tracker.auth import login_manager, auth
    from audit_tracker.auditor_page import status
    from audit_tracker.admin_report import report
    from audit_tracker.config import get_connection
    from audit_tracker.upload import file
    from audit_tracker.down_report import download
    from audit_tracker.test import only_one
    from audit_tracker.database import mango_base
    from audit_tracker.smtp import mail_bp
    from audit_tracker.audit_log import audit_log
    from audit_tracker.apply import audit_bp
    from audit_tracker.whatsappweb import application

    app = Flask(__name__)

    # Flask-Login setup
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Mail server configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', '')

    # Initialize mail with app
    mail.init_app(app)

    # Persistent secret key & session lifetime
    app.secret_key = os.getenv('SECRET_KEY', 'audit_avengers_secret_key_2025_prod_secure')
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    app.permanent_session_lifetime = timedelta(hours=2)

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(report)
    app.register_blueprint(file)
    app.register_blueprint(status, name="status_blueprint")
    app.register_blueprint(download)
    app.register_blueprint(mango_base)
    app.register_blueprint(audit_log)
    app.register_blueprint(mail_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(application)

    @app.route('/')
    def home():
        return render_template('home.html')

    # Login Page
    @app.route('/login_page')
    def login_view():
        return render_template('login.html')

    # Signup Page
    @app.route('/signup_page')
    def signup_view():
        return render_template('signup.html')

    # Dashboard (Protected)
    @app.route('/admin/dashboard')
    @login_required
    @only_one('admin')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/report')
    @login_required
    @only_one('admin')
    def repo():
        return render_template('admin_report.html')

    @app.route('/admin/manual_data')
    @login_required
    @only_one('admin')
    def new_data():
        return render_template('manual_data.html')

    @app.route('/application')
    @login_required
    @only_one('admin')
    def application_page():
        return render_template('application.html')

    @app.route('/audit_card', methods=['GET'])
    def card():
        return render_template('audit_card.html')

    return app

