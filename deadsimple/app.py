# http://flask.pocoo.org/docs/1.0/config/

import os
import time
import bcrypt
import random
from flask import Flask, session, redirect, render_template, url_for, request
from flask import flash
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///deadsimple.db', echo=True)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return redirect('/account')

@app.route("/signup", methods=['GET'])
def do_signup():
    return render_template('signup.html')

@app.route("/create-user", methods=['POST'])
def do_create_user():
    POST_FIRST = request.form['first']
    POST_LAST = request.form['last']
    POST_EMAIL = request.form['email']
    POST_PASSWORD = request.form['password']
    POST_NUMBER = request.form['phone']

    POST_PASSWORD_BYTES = bytes(POST_PASSWORD, 'utf-8')
    POST_PASSWORD_ENCRYPTED = bcrypt.hashpw(POST_PASSWORD_BYTES, bcrypt.gensalt())

    Session = sessionmaker(bind=engine)
    s = Session()

    user = User(POST_FIRST, POST_LAST, POST_EMAIL, POST_PASSWORD_ENCRYPTED, POST_NUMBER)
    s.add(user)
    s.commit()

    return redirect('/login')

@app.route("/login")
def do_login():
    return render_template('login.html')

@app.route("/authenticate", methods=['POST'])
def do_authenticate():
    POST_EMAIL = request.form['email']
    POST_PASSWORD = request.form['password']

    POST_PASSWORD_BYTES = bytes(POST_PASSWORD, 'utf-8')
    POST_PASSWORD_ENCRYPTED = bcrypt.hashpw(POST_PASSWORD_BYTES, bcrypt.gensalt())

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.email.in_([POST_EMAIL]))
    user = query.first()

    print(user.password)
    print(POST_PASSWORD_ENCRYPTED)

    if bcrypt.checkpw(POST_PASSWORD_BYTES, user.password):
        session['logged_in'] = True
        session['email'] = user.email
        session['id'] = user.id
    else:
        flash('Wrong password!')

    return redirect('/')

@app.route("/account")
def do_account_setup():
    if session['logged_in'] is True:
        return render_template('account.html')
    else:
        return redirect('/')

@app.route("/logout")
def do_logout():
    session['logged_in']=False
    return redirect('/')

days = {"Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
       }

emoji = {"Monday": [u'\U0001f607', u'\U0001f61f'],
         "Tuesday": [u'\U0001f61b', u'\U0001f928'],
         "Wednesday": [u'\U0001f62c', u'\U0001f634'],
         "Thursday": [u'\U0001f915', u'\U0001f635'],
         "Friday": [u'\U0001f60e', u'\U0001f600'],
         "Saturday": [u'\U0001f600', u'\U0001f643'],
         "Sunday": [u'\U0001f604']
        }

@app.route("/workout")
def show_workout():

    day_text = request.args.get('day', 'Monday')
    day = days[day_text]
    user_id = session['id']

    Session = sessionmaker(bind=engine)
    s = Session()
    result = s.query(Exercise).filter(Exercise.user_id == user_id, Exercise.day == day, Exercise.deleted == False)

    random_emoji = random.choice(emoji[day_text])

    return render_template('workout.html', day=day_text, emoji=random_emoji, data=result)

@app.route("/add-exercise", methods = ['POST'])
def do_add_exercise():
    user_id = session['id']
    day_text = request.args.get('day', 'Monday')
    day = days[day_text]
    type = request.form['type']
    weight = request.form['weight']
    reps = request.form['reps']
    deleted = False

    Session = sessionmaker(bind=engine)
    s = Session()

    exercise = Exercise(user_id, day, type, weight, reps, deleted)
    s.add(exercise)
    s.commit()

    return redirect(f'/workout?day={day_text}')

@app.route("/delete-exercise", methods = ['POST'])
# Make this work: https://stackoverflow.com/questions/3915917/make-a-link-use-post-instead-of-get
def do_delete_exercise():
    # Does this need a default value?
    id = request.args.get('id')
    day = request.args.get('day')

    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(Exercise).filter(Exercise.id == id)
    exercise_to_delete = query.first()
    exercise_to_delete.deleted = True
    s.commit()

    return redirect(f'/workout?day={day}')

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    user_number_raw = request.values.get('From')

    # This is a hack to remove the country code.
    user_number = user_number_raw[2:]

    message = request.values.get('Body')
    localtime = time.localtime(time.time())
    resp = MessagingResponse()

    if message == 'Y':
        Session = sessionmaker(bind=engine)
        s = Session()

        query = s.query(User).filter(User.phone == user_number)
        user = query.first()
        exercises = s.query(Scheduled_Exercise).filter(Scheduled_Exercise.user_id == user.id, Scheduled_Exercise.day == localtime[6], Scheduled_Exercise.done == False)
        first_exercise = exercises.first()
        resp.message(f"All right, go do {first_exercise.type}, {first_exercise.weight} pounds, {first_exercise.reps} reps. Reply 'D' when you're done.")
        last_exercise = first_exercise

    elif message == 'D':
        Session = sessionmaker(bind=engine)
        s = Session()

        query = s.query(User).filter(User.phone == user_number)
        user = query.first()
        exercises = s.query(Scheduled_Exercise).filter(Scheduled_Exercise.user_id == user.id, Scheduled_Exercise.day == localtime[6], Scheduled_Exercise.done == False)
        last_exercise = exercises.first()
        last_exercise.done = True

        exercises = s.query(Scheduled_Exercise).filter(Scheduled_Exercise.user_id == user.id, Scheduled_Exercise.day == localtime[6], Scheduled_Exercise.done == False)

        if len(exercises.all()) != 0:
            next_exercise = exercises.first()
            resp.message(f"All right, go do {next_exercise.type}, {next_exercise.weight} pounds, {next_exercise.reps} reps. Reply 'D' when you're done.")

        elif len(exercises.all()) == 0:
            resp.message("Great workout today! See you next time!")

        s.commit()

    else:
        resp.message("OK, see you next time!")

    return str(resp)

print(app.config)

if __name__ == "__main__":
    app.run()
