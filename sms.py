# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_AUTH']
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Hello there!',
                              from_='+12056277820',
                              media_url=['https://demo.twilio.com/owl.png'],
                              to='+16266366223'
                          )

print(message.sid)
