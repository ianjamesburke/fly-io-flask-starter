from functools import wraps
from flask import session, redirect, url_for, flash, request
from supabase import create_client, Client
import os


# Check for Supabase environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise EnvironmentError("Supabase URL and Key must be set in environment variables.")

# Initialize Supabase client
supabase: Client = create_client(url, key)

print(f"Supabase URL: {url}")  # Debug log
print(f"Supabase key length: {len(key) if key else 'None'}")  # Debug log

try:
    # Test the connection
    test = supabase.auth.get_session()
    print("Supabase connection successful")
except Exception as e:
    print(f"Supabase connection error: {str(e)}")

def login_user(email, password):
    """Login user with email and password"""
    try:
        print(f"Attempting login for email: {email}")  # Debug log
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print(f"Login response: {response}")  # Debug log
        session['user'] = {
            'id': response.user.id,
            'email': response.user.email,
            'access_token': response.session.access_token
        }
        return True, "Login successful"
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        return False, str(e)


def register_user(email, password):
    """Register new user with email/password"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return True, "Registration successful. Please check your email to verify your account."
    except Exception as e:
        return False, str(e)

def logout_user():
    """Logout user"""
    try:
        supabase.auth.sign_out()
        session.clear()
        return True, "Logout successful"
    except Exception as e:
        return False, str(e)

def is_authenticated():
    """Check if user is authenticated"""
    return 'user' in session

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current user from session"""
    return session.get('user')