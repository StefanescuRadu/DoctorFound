# DoctorFound
E-Health App

Users can join our site when they have an emergency i.e. 'toothache' and look for a doctor.

"Why can't I just use google????"

The reasons:

At first, the users need to login with google (used google for credibility and security). We also store their email in our database, so we can send users follow-up emails with the experienced. We will store the review in our own database, and on the future, we will leave some details for every cabinet depending on what the pacients experience (and adjust our recommandations accordingly)

Upon searching for the emergency, we use google maps to retrive the first 20 nearest 'cabinets' closest to the user ordered by the closeset, since it's an emergency. (on the future we might used the searched based on our customers reviews)

The user can click next to view the next cabinet if he decides so, or previous.

A map is also shown, so that the user can see in real time the distance to the cabinet.


The user can purchase a premium account for some extra benefits:
    -A one on one live chat with one of our medics
    -Our customs reviews(left by the customers)- Not implemented yet



How to install:

virtualenv -p python3 venv
python3 -m venv venv
pip3 install -r requirements.txt
create the .env file (rename the .env_template to .env)
Create the mockup tables in a new database by running the test.sql
python3 server.py





Credits:
Create login with google: https://github.com/Vuka951/tutorial-code/tree/master/flask-google-oauth2
Video Chat: https://github.com/sayantanDs/webrtc-videochat