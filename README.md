# 💌 Postcrafts
Welcome to Postcrafts, a web application for designing and sending e-cards via text or email to friends and family. Through Postcrafts, users can create cards from scratch or pick from pre-designed card templates.
![Postcraft page](https://res.cloudinary.com/dejqcmvuw/image/upload/v1657408536/Postcrafts_lkniks.png)

# 🧭 Table of Contents
- [Technologies](https://github.com/gingercw/postcrafts/edit/main/README.md#technologies)
- [Features](https://github.com/gingercw/postcrafts/edit/main/README.md#features)
- [Future Development](https://github.com/gingercw/postcrafts/edit/main/README.md#future-development)
- [Installation](https://github.com/gingercw/postcrafts/edit/main/README.md#installation)

# 🤖 Technologies
### Tech Stack
- Python
- Flask
- Jinja
- Javascript
- AJAX
- PostgreSQL
- SQLAlchemy
- HTML
- CSS
- Bootstrap

### APIs and Libraries
- [Filerobot Image Editor](https://scaleflex.github.io/filerobot-image-editor/)
- [Unsplash API](https://unsplash.com/developers)
- [Cloudinary API](https://cloudinary.com/)
- [Twilio API](https://www.twilio.com/)
- [SendGrid SMTP Email](https://sendgrid.com/)

# 🏔️ Features
Postcrafts offers a robust set of features for designing and sending e-cards. 

### 🎨 Design a Card
Users can search and select images for the card's background. They can then add filters, text, and shapes with Filerobot's built in design tools. Once the design is complete, users can save it to their cards.

### 👯 Pick a Template
Users can search through published templates and add the ones they like to their card collection.

### 🎬 Card Actions
- **Send a Card:** Users can add a personalized message to their card and send it to a contact in their Address Book. The application can send the card by text or email.
- **Publish Card:** To make the card public, users can publish cards they created as templates for others on the site to use.
- **Edit Cards:** Users can edit a card they created or a template to customize it.
- **Delete:** To make room for more cards, users can hit "Delete" to remove cards from their collection. 

### 📇 Address Book
Users can add contacts to the Address Book so to send cards. The Address Book supports text and email.

### 📬 Outbox
Users can view a history of all the cards and messages they've sent in their Outbox.

# 🔮 Future Development
The next stage of Postcrafts includes:
- Create HTML templates for emails. 
- Sending cards as physical mail through the USPS.
- Categorizing templates by holidays and events.
- Scheduling cards to be sent.
- Improving user verification. 

# 🪛 Installation
**Requirements:**
- PostgreSQL
- Twilio account
- SendGrid account
- Cloudinary account

**1. Clone or fork the repo and open it in your IDE.**
```
https://github.com/gingercw/postcrafts
```

**2. Create and activate a virtual environment inside the directory.**
```
$ virtualenv env
$ source env/bin/activate
```

**3. Install the dependencies.**
```
$ pip install -r requirements.txt
```

**4. Set up the database.**
```
$ createdb cards
$ python3 model.py
$ python3 seed_database.py
```

**5. Run the server.**
```
$ python3 server.py
```
