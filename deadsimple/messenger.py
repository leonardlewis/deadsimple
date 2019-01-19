from twilio_client import client, number
# Configure a Cron job to send a workout message every day at 8am.

# Look up all the users in the database who have exercises for the current day of the week.


# For each user in the query, send a message to their number.
# Send a message to the user: "You're ready to workout! Reply "Y" to start or
# N to cancel.
start_message = client.messages.create(
        to="+12164029029",
        from_=number,
        body="Good morning! Please reply 'Y' to start your Deadsimple workout or 'N' to cancel for today.")

print(start_message.sid)

# Receive response from user and reply "Your first exercise is X" or "OK, see you
# tomorrow!"
