from flask import Flask, request, make_response, redirect, url_for
import firebase_admin
from firebase_admin import auth, credentials
app = Flask(__name__)
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred)
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.get_user_by_email(email)
        id_token = auth.create_custom_token(user.uid)
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('token', id_token, httponly=True, secure=True)  # Secure and HttpOnly flags for safety
        return response
    except Exception as e:
        return f"Error: {str(e)}", 400
