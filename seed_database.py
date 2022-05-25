"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb cards")
os.system("createdb cards")

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    db_user = crud.create_user(email, password)
    model.db.session.add(db_user)

    # TODO: create 10 ratings for the user


    for x in range(5):
      recipient=f'recipient{x}'
      street_address = f'{n} Test St.'
      city = 'New York City'
      state = 'NY'
      zipcode = 12345
      hidden = False

      db_address = crud.create_address(recipient, street_address, city, state, zipcode, hidden, db_user)
      model.db.session.add(db_address)

    for x in range(10):
      title = f'card{x}'
      url = "https://picsum.photos/300/200"
      published = False
      hidden = False

      db_card = crud.create_card(title, url, published, hidden, db_user)
      model.db.session.add(db_card)

      for y in range (5):
        message = f'Hi person{y}--check out where I went!'
        date_sent = f"2022-5-{y + 1}"
        
        db_sentcard = crud.create_sentcard(message, date_sent, db_card, db_address)
        model.db.session.add(db_sentcard)


        

model.db.session.commit()


