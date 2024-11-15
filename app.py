### INIT ###

if os.environ.get('FLASK_APP'):
    print("Running in production")

else:
    print("Running in development")
    print("Loading dotenv")
    from dotenv import load_dotenv
    load_dotenv()





### IMPORTS ###

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from auth_module import login_user, register_user, logout_user, login_required, is_authenticated
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key')  # Change this in production




### SUPABASE ###
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise EnvironmentError("Supabase URL and Key must be set in environment variables.")

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key)






@app.route('/')
# @login_required
def home():
    user_email = session.get('user', {}).get('email', None)
    return render_template('index.html', user_email=user_email)



# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Login attempt with email: {email}")  # Debug log
        success, message = login_user(email, password)
        print(f"Login result: success={success}, message={message}")  # Debug log
        
        if success:
            return redirect(url_for('home'))
        flash(message, 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_authenticated():
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        success, message = register_user(email, password)
        flash(message, 'success' if success else 'error')
        if success:
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)