from twilio.rest import Client

account_sid = "ACf8315151a6829b1fdd78562df9efac7d"
auth_token = "264c6507b58352dc7ef941b01b3edbea"
number = "+14402765490"


client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+12164029029",
    from_=number,
    body="Hello, World!")

print(message.sid)
