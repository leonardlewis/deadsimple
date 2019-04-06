# https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/
# https://crontab.guru

import os
import time
from twilio_client import client, number
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import extract
from tabledef import *
engine = create_engine(os.environ['DATABASE_URL'], echo=True)

# Configure a Cron job to send a workout message every day at 8am.

# Look up all the users in the database who have exercises for the current day of the week.
localtime = time.localtime(time.time())
Session = sessionmaker(bind=engine)
s = Session()
query = s.query(Scheduled_Exercise).filter(Scheduled_Exercise.day == localtime[6])

# Create a deduplicated list of user IDs from the query.
users = set()
for x in query:
    users.add(x.user_id)

# For each user in the query, send a message to their number.
for x in users:
    recipient = s.query(User).filter(User.id == x)
    for y in recipient:
        to_number = y.phone
        start_message = client.messages.create(
            to = str(to_number),
            from_=number,
            body="Good morning! Please reply 'Y' to start your Dead Simple workout or 'N' to cancel for today.")
        print(start_message.sid)
