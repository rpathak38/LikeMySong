from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
import mysql.connector, csv
import pandas as pd
from spotify_client import *
from googlesearch import search
import search_google
from pickles import pickles
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="music123",
    database="musicdb"
)

mycursor = mydb.cursor()

client_id = 'bbd7a9b053844b45b1bbe801383e8b2b' # '' = your client_id
client_secret = '7d8cd9c307434f48b49264348e5c3d00' # '' = your client_secret
spotify = SpotifyAPI(client_id, client_secret)

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    #instantiate Spotify API Client Object (SAPICO)
    user = None
    if request.method == 'POST':
        user = request.form['nm']
    if user != None:
        user_song_id = user
        mycursor.execute("SELECT cluster FROM ml_results WHERE id=%s", (user_song_id,))
        output = mycursor.fetchall()
        
        if not output:
            client = spotify.get_track_audio_features(user_song_id)
            features = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness',
                        'loudness', 'speechiness', 'tempo']
            input_data = []
            for feature in features:
                input_data.append(client[feature])
            input_data = np.array(input_data)
            cluster = pickles.online_training(input_data)
            cluster = cluster[0].item()
            sql = "INSERT INTO ml_results (id, cluster) VALUES (%s, %s)"
            val = (user_song_id, cluster)
            mycursor.execute(sql, val)
            mydb.commit()
        else:    
            cluster = output[0][0]

        mycursor.execute("SELECT id FROM ml_results WHERE cluster=%s", (cluster,))
        result = mycursor.fetchall()
        #TODO explicit used as a filter, defaults to non-explicit
        song_rec_ids = []
        for item in result:
            song_rec_ids.append(item[0])
        song_rec_ids.remove(user_song_id)
        recs = []
        for id in song_rec_ids:
            recs.append(spotify.get_track_specific_data(id))

        data = {}
        for rec in recs:
            data[rec] = 'https://open.spotify.com/track/' + spotify.get_track_specific_data(id, 'uri')[14:]

        print(data)
        
        
    return render_template('home.html')

@app.route("/about", methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        user = request.form['nm']

        try:
            id5 = search_google.google_search(user)
            data = []

            for id in id5:
                artist_ids = spotify.get_track_artists_id(id)
                artists = []
                for artist_id in artist_ids:
                    artists.append(spotify.get_artist_specific_data(artist_id))
                data.append((spotify.get_track_specific_data(id), artists, id))

            print(data)
        except search_google.SongNotFound as e:
            print(e.message)

    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        val = (form.username.data, form.email.data, form.password.data)
        mycursor.execute(sql, val)
        mydb.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_password = None
        mycursor.execute("SELECT password FROM users WHERE email=%s", (form.email.data,))
        output = mycursor.fetchall()
        for item in output:
            user_password = item[0]
        if user_password == None:
            mycursor.execute("SELECT password FROM users WHERE username=%s", (form.email.data,))
            output = mycursor.fetchall()
            print(form.email.data)
            print(output)
            for item in output:
                user_password = item[0]
        if form.password.data == user_password:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    
