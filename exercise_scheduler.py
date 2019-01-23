## After you get this working, write a shell script that executes it. The
## Cron job will run that shell script.
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *


# Look up exercises scheduled for today.
localtime = time.localtime(time.time())
Session = sessionmaker(bind=engine)
s = Session()
query = s.query(Exercise).filter(Exercise.day == localtime[6])

# Create timestamped rows in the scheduled_exercises schedule.
Session = sessionmaker(bind=engine)
s = Session()

for x in query:
    user_id = x.user_id
    day = x.day
    type = x.type
    weight = x.weight
    reps = x.reps
    exercise_id = x.id
    date = '2019-1-23'
    done = False

    # Script is adding to Exercises table, so maybe make Scheduled_Exercise not a child.
    scheduled_exercise = Scheduled_Exercise(user_id, day, type, weight, reps,
                                            exercise_id, date, done)
    s.add(scheduled_exercise)
    s.commit()
