from flask import Flask, render_template, redirect, url_for, session, flash, request
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from dotenv import load_dotenv
from datetime import datetime

import datamanager
import util

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        searched = request.form.get('search-box') #for dragos



    premium = '1999'
    current_date = util.get_current_datetime()
    print("current_date: 0000000")
    print(current_date)
    print(type(current_date))
    print('-----------0-------------')
    if 'profile' in session:
        email = session['profile']['email']
        try:  # index error if email not found in the databse/ not registered
            datamanager.check_if_user_exists(email)[0]['email']
        except IndexError:
            datamanager.add_user(email)

        premium = datamanager.check_if_premium(email)[0]['premium_expiration']
        print('premium: 00000')
        print(premium)
        print(type(current_date))
        print('-----------0-------------')
    return render_template('main.html', premium=premium, current_date=current_date)


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/premium/<email>', methods=['GET', 'POST'])
def buy_premium(email):
    email = email.replace('}', '')
    print(email)
    if request.method == 'POST':
        if request.form.get('voucher') == 'reducere':
            datamanager.give_premium(email)
    print('----------')
    print(str(session))
    print('----------')
    return render_template('premium.html')


if __name__ == '__main__':
    app.run(debug=True)