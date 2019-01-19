import time
from twilio_client import client, number
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import extract
from tabledef import *
engine = create_engine('sqlite:///deadsimple.db', echo=True)

# Configure a Cron job to send a workout message every day at 8am.

# Look up all the users in the database who have exercises for the current day of the week.
localtime = time.localtime(time.time())
Session = sessionmaker(bind=engine)
s = Session()
query = s.query(Exercise).filter(Exercise.day == localtime[6])

# Create a deduplicated list of user IDs from the query.
users = set()
for x in query:
    users.add(x.user_id)

print(users)

# For each user in the query, send a message to their number.
# Send a message to the user: "You're ready to workout! Reply "Y" to start or
# N to cancel.
# start_message = client.messages.create(
#        to="+12164029029",
#        from_=number,
#        body="Good morning! Please reply 'Y' to start your Dead Simple workout or 'N' to cancel for today.")

# print(start_message.sid)

# Receive response from user and reply "Your first exercise is X" or "OK, see you
# tomorrow!"
