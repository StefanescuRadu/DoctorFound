from google_api_folder.places import places
from flask import Flask, render_template, redirect, url_for, session, flash, request, send_from_directory
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from dotenv import load_dotenv
from datetime import datetime
from flask_socketio import SocketIO, emit, join_room, leave_room
import googlemaps


import datamanager
import util


_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users


from engineio.payload import Payload
Payload.max_decode_packets = 200

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
socketio = SocketIO(app)


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
# Gmaps Setup
gmaps = googlemaps.Client(key=app.secret_key)


@app.route('/', methods=['GET', 'POST'])
def main():
    
    if request.method == 'POST':
        search_string = request.form.get('search-box',"urgente medicale generale")
        datamanager.add_search_history(session['profile']['email'], search_string)
        current_home_address=request.form.get('current_location',"Strada Semilunei 4-6, București 020797")
    else:
        search_string = "urgente medicale generale"
        current_home_address="Strada Semilunei 4-6, București 020797"
    
    geocode_home_address = util.convert_address(gmaps.geocode(current_home_address)[0])
    locations = places(gmaps,query=search_string,location=geocode_home_address['geometry'],radius=5000,language="ro",type="doctor")
    sorted_locations = util.get_clean_closest_locations(locations,geocode_home_address)
    
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
        # TODO: Sa modific in loc de index 0, index de i, sau ce imi da
        try:
            if not len(datamanager.check_if_cabinet_exists(sorted_locations[0]['place_id'])) > 0:
                # print(datamanager.check_if_cabinet_exists(sorted_locations[0]['place_id']))'
                datamanager.add_cabinet(sorted_locations[0])
            # TODO: Sa verific daca merge
        except IndexError:
            return render_template('main.html', premium=premium, current_date=current_date, sorted_locations=sorted_locations)
    print('-----------1-------------')
    print(str(sorted_locations[0]))
    print('-----------1-------------')
    sorted_locations[0]['temp_distance'] = str(round(sorted_locations[0]['temp_distance'],2))
    return render_template('main.html', premium=premium, current_date=current_date, sorted_locations=sorted_locations)


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
    # print(email)
    if request.method == 'POST':
        if request.form.get('voucher') == 'reducere':
            datamanager.give_premium(email)
    # print('----------')
    # print(str(session))
    # print('----------')
    return render_template('premium.html')


# @app.route("/join", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         room_id = 'drFound'
#         return redirect(url_for("entry_checkpoint", room_id=room_id))
#
#     return render_template("home.html")


@app.route("/room/<string:room_id>/")
def enter_room(room_id):
    search_string = "urgente medicale generale"
    current_home_address = "Strada Semilunei 4-6, București 020797"
    geocode_home_address = util.convert_address(gmaps.geocode(current_home_address)[0])
    locations = places(gmaps, query=search_string, location=geocode_home_address['geometry'], radius=5000, language="ro",
                   type="doctor")
    sorted_locations = util.get_clean_closest_locations(locations, geocode_home_address)
    premium = '1999'
    if room_id not in session:
        return redirect(url_for("entry_checkpoint", room_id=room_id))
    if 'profile' in session:
        email = session['profile']['email']
        premium = datamanager.check_if_premium(email)[0]['premium_expiration']
    current_date = util.get_current_datetime()
    return render_template("main.html", room_id=room_id, display_name=session[room_id]["name"],sorted_locations=sorted_locations,
                           mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"], premium=premium, current_date=current_date)


@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    if request.method == "POST":
        display_name = session['profile']['given_name']
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": display_name, "mute_audio": mute_audio, "mute_video": mute_video}
        session['joined'] = 'yes'
        return redirect(url_for("enter_room", room_id=room_id))

    return render_template("chatroom_checkpoint.html", room_id=room_id)


@socketio.on("connect")
def on_connect():
    sid = request.sid
    print("New socket connected ", sid)


@socketio.on("join-room")
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]

    # register sid to the room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    _name_of_sid[sid] = display_name

    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)

    # add to user list maintained on server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid})  # send own id only
    else:
        usrlist = {u_id: _name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid})  # send list of existing users to the new member
        _users_in_room[room_id].append(sid)  # add new member to user list maintained on server

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    room_id = _room_of_sid[sid]
    display_name = _name_of_sid[sid]

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)
    if len(_users_in_room[room_id]) == 0:
        _users_in_room.pop(room_id)

    _room_of_sid.pop(sid)
    _name_of_sid.pop(sid)

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("data")
def on_data(data):
    sender_sid = data['sender_id']
    target_sid = data['target_id']
    if sender_sid != request.sid:
        print("[Not supposed to happen!] request.sid and sender_id don't match!!!")
    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))
    socketio.emit('data', data, room=target_sid)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')



if __name__ == '__main__':
    app.run(debug=True)