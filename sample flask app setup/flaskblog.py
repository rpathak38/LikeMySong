from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import mysql.connector, csv
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="music123",
    database="musicdb"
)

mycursor = mydb.cursor()

@app.route("/")
@app.route("/home", methods = ['POST']
def home():
    #didn't really touch the other code yet, but this is the db implementation
    #the input will be assigned to user_song_id and for now, i returned a
    #list of the song ids in song_rec_ids
    #any other querying/ranking can be done from this point
    user_song_id = '5dl96yjlEqgrZ74QwQqqYW'
    mycursor.execute("SELECT cluster FROM ml_results WHERE id=%s", (user_song_id,))
    cluster = mycursor.fetchall()[0][0]
    mycursor.execute("SELECT id FROM ml_results WHERE cluster=%s", (cluster,))
    result = mycursor.fetchall()
    song_rec_ids = []
    for item in result:
        song_rec_ids.append(item[0])
    song_rec_ids.remove(user_song_id)
    
    return render_template('home.html', posts=posts)
    
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
