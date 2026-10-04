import os
from functools import wraps
from flask_login import current_user
from flask import session, redirect

def only_one(*roles):
    def decorator(func):
        @wraps(func)
        def checker(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect('/signup_page')
            
            user_role = session.get('role')
            user_name = session.get('username')
            admin_username = os.getenv('ADMIN_USERNAME', 'Admin@raghu')

            if 'admin' in roles:
                if user_role != 'admin' and user_name != admin_username:
                    return redirect('/signup_page')
            elif 'auditor' in roles:
                if user_role != 'auditor':
                    return redirect('/signup_page')
            
            return func(*args, **kwargs)
        return checker
    return decorator


