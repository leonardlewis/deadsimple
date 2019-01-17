# http://blog.appliedinformaticsinc.com/managing-cron-jobs-with-python-crontab/
# https://vitalets.github.io/combodate/

from flask import Flask, session, redirect, render_template, url_for, request
from flask import flash, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///deadsimple.db', echo=True)

app = Flask(__name__)

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

    Session = sessionmaker(bind=engine)
    s = Session()

    # Set logged_in to False when user gets created.
    user = User(POST_FIRST, POST_LAST, POST_EMAIL, POST_PASSWORD, POST_NUMBER, False)
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

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.email.in_([POST_EMAIL]), User.password.in_([POST_PASSWORD]))
    user = query.first()
    if user:
        session['logged_in'] = True
        session['email'] = user.email
        session['id'] = user.id
        user.logged_in = True
        s.commit()
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

@app.route("/workout")
def show_workout():
    day = request.args.get('day', 'monday')
    user_id = session['id']

    Session = sessionmaker(bind=engine)
    s = Session()
    result = s.query(Exercise).filter(Exercise.user_id == user_id, Exercise.day == day)

    return render_template('workout.html', day=day, data=result)

@app.route("/add-exercise", methods = ['POST'])
def do_add_exercise():
    user_id = session['id']
    day = request.args.get('day', 'Monday')
    type = request.form['type']
    weight = request.form['weight']
    reps = request.form['reps']

    Session = sessionmaker(bind=engine)
    s = Session()

    exercise = Exercise(user_id, day, type, weight, reps)
    s.add(exercise)
    s.commit()

    return redirect(f'/workout?day={day}')

@app.route("/delete-exercise", methods = ['POST'])
# Make this work: https://stackoverflow.com/questions/3915917/make-a-link-use-post-instead-of-get
def do_delete_exercise():
    # Does this need a default value?
    id = request.args.get('id')
    day = request.args.get('day')

    Session = sessionmaker(bind=engine)
    s = Session()

    s.query(Exercise).filter(Exercise.id == id).\
        delete(synchronize_session=False)
    s.commit()

    return redirect(f'/workout?day={day}')

# YOU SHOULD CHANGE THIS WHEN YOU PUT ON THE INTERNET
app.secret_key = b'\xc0\xac~\x1f\xa8\xd6\x0c)\x16-:\xbeC\xef{\xab'

if __name__ == "__main__":
    app.run()
