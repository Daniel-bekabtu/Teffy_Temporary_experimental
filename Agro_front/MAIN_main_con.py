from flask import Flask, render_template, redirect, request, session, url_for, jsonify, make_response
import firebase_admin
from firebase_admin import credentials, auth, db, storage
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '1111'

cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tchat-af17d-default-rtdb.firebaseio.com',
    'storageBucket': 'tchat-af17d.appspot.com'
})

def is_logged_in():
    return 'uid' in session

@app.route('/')
def home():
    return render_template('Front_page_1.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_id = request.cookies.get('uid')
        ref = db.reference(f'users/{user_id}')
        user_data = ref.get()
        if user_data:
            return jsonify({'user_data': user_data})
        else:
            return jsonify({'message': 'User not found'}), 404
    return render_template('login_page_Session_checked_1.html')

@app.route('/register_farm_land', methods=['POST', 'GET'])
def register_farm_form():
    if(request.method == "POST"):
        user_id = request.cookies.get('uid')
        print(user_id)
        form_data = {
            'owner_user_id': user_id,
            'farmName': request.form['farmName'],
            'ownerName': request.form['ownerName'],
            'contactPhone': request.form['contactPhone'],
            'contactEmail': request.form['contactEmail'],
            'nationality': request.form['nationality'],
            'region': request.form['region'],
            'farmAddress': request.form['farmAddress'],
            'latitude': request.form['latitude'],
            'longitude': request.form['longitude'],
            'elevation': request.form['elevation'],
            'totalArea': request.form['totalArea'],
            'accessRoads': request.form['accessRoads'],
            'farmType': request.form['farmType'],
            'mainCrops': request.form['mainCrops'],
            'farmingPractice': request.form['farmingPractice'],
            'waterSource': request.form['waterSource'],
            'soilType': request.form['soilType'],
            'infrastructure': request.form['infrastructure'],
            'fundAmount': request.form['fundAmount'],
            'fundingPurpose': request.form['fundingPurpose'],
            'returnRate': request.form['returnRate'],
            'paybackPeriod': request.form['paybackPeriod'],
            'collateral': request.form['collateral'],
            'currentRevenue': request.form['currentRevenue'],
        }
        hardcoded_url = "https://www.istockphoto.com/photo/aerial-view-of-fields-and-farmland-gm1263711041-369949935?utm_source=pixabay&utm_medium=affiliate&utm_campaign=sponsored_image&utm_content=srp_topbanner_media&utm_term=farmland"
        land_title_url = hardcoded_url
        farm_image_urls = hardcoded_url
        certification_urls = hardcoded_url  
        form_data['landTitle'] = land_title_url
        form_data['farmImages'] = farm_image_urls
        form_data['certifications'] = certification_urls
        ref = db.reference(f'users/{user_id}/land').push()
        ref.set(form_data)
        return jsonify({"message": "Farm registration successful!"}), 200
    return render_template("register_farm_land.html")
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        uid = data.get('uid')
        if not uid:
            return jsonify({'message': 'UID missing'}), 400
        response = make_response(jsonify(url_for("login")))
        response.set_cookie('uid', uid)
        return response
    return render_template('Get_started_Sign_up_2.html')

@app.route('/User_fetch_request', methods=["POST", "GET"])
def User_fetch_uid():
    if request.method == "POST":
        user_id = request.cookies.get('uid')
        if user_id:
            return jsonify({'user_id': user_id})
        else:
            return jsonify({'message': 'User not found'}), 404
    return render_template('login_page_Session_checked_1.html')
@app.route('/Role_fetch_request', methods=["POST", "GET"])
def Role_fetch_uid():
    if request.method == "POST":
        user_id = request.cookies.get('uid')
        user_ref = db.reference(f'users/{user_id}/role')
        role = user_ref.get()
        print(role)
        if(role == "farmer"):
            return jsonify({"role":"farmer"})
        if (role == "investor"):
            return jsonify({"role":"investor"})
        else:
            return jsonify({'message': 'Role not found'}), 404
    return render_template('login_page_Session_checked_1.html')

@app.route('/farmer-dashboard')
def farmer_dashboard():
    return render_template('Famer_Dashboard.html')

@app.route('/invester-dashboard')
def invester_dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('Invester_Dashboard.html')

@app.route('/learn-more')
def learn_more():
    return render_template('Learn_more_2.html')

@app.route('/register-farm')
def register_farm():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('register_farm_land.html')
@app.route('/signin-selection')
def signin_selection():
    return render_template('Sign_in_login_fd_selecion.html')
@app.route('/my-lands')
def my_lands_route():
    return render_template('My_lands.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/reports', methods=["POST", "GET"])
def report_fetch_R():
    #fetch logic here ----> trFDx
    return render_template('farmer_report.html')
@app.route('/funds', methods=["POST", "GET"])
def funds_cardano_base_main():
    #cardano-smartcont logic here ----> trFDd
    return render_template('Farmer_funds_eff.html')
if __name__ == '__main__':
    app.run(debug=True)
