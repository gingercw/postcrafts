"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, Markup)

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from twilio.rest import Client

from model import connect_to_db, db

from datetime import datetime

import crud 

from jinja2 import StrictUndefined

import os

import requests



app = Flask(__name__)
app.secret_key = "APIKEY"
app.jinja_env.undefined = StrictUndefined

CLIENTID = os.environ['CLIENTID']
CLOUDINARY_URL = os.environ['CLOUDINARY_URL']

account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_AUTH']
client = Client(account_sid, auth_token)

@app.route('/')
def index():
    """go to homepage if a user is not already logged in"""
    if "user_id" in session:
        user_id = session.get("user_id")
        return redirect(f"/{user_id}")
    else:
        return render_template("homepage.html")

@app.route('/<user_id>/new_card')
def make_card(user_id):
    """create a new card"""
    user_details = crud.get_user_by_id(user_id)
    
    return render_template("new_card.html", user_details=user_details)


@app.route('/<user_id>')
@app.route('/<user_id>/')
def get_user_details(user_id):
    """show user profile page with created cards"""
    user_details = crud.get_user_by_id(user_id)
    users_cards = crud.get_cards_by_user(user_id)
    cards_sent = crud.get_sent_cards_by_user(user_id)
    contacts = crud.get_contacts_by_user(user_id)


    return render_template("user_profile.html", user = user_details, cards = users_cards, sent_cards = cards_sent, contacts = contacts)


@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""
    user_email = request.form.get("email")
    password = request.form.get("password")

    email_check = crud.get_user_by_email(user_email)

    if email_check is None:
        new_user = crud.create_user(user_email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Whoo hoo! Log in to start creating.")
    else:
        flash("An account already exists with that email. Try logging in.")
    return redirect("/")
    

@app.route("/login", methods=["POST"])
def login():
    """log in existing user"""
    input_email = request.form.get("email")
    input_password = request.form.get("password")

    user = crud.get_user_by_email(input_email)

    if not user:
        flash("No account exists with that email")
        return redirect('/')
    elif input_password == user.password:
        user_id = user.user_id
        session["user_id"] = user_id
        return redirect(f"/{user_id}")
    else:
        flash("Wrong password")
        return redirect("/")

@app.route("/logout")
def logout():
    """log out user"""
    del session["user_id"]
    flash("You logged out. Thanks for crafting!")
    return redirect("/")
        
@app.route('/photos')
def get_photos():
    """View the details of an event."""
    place = request.args.get("location")
    headers_dict = {"Authorization": f"Client-ID {CLIENTID}"}

    url = f'https://api.unsplash.com/photos/random?query={place}&orientation=landscape&count=8'

    response = requests.get(url, headers=headers_dict)

    return response.text



@app.route('/save', methods=["POST"])
def save_card():
    """save card to database"""
    title = request.json.get("title")
    raw_image = request.json.get("rawImage")
    upload_result = upload(raw_image)
    url, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=300, height=200)
    published = False
    hidden = False
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    card = crud.create_card(title, url, published, hidden, user)
    
    db.session.add(card)
    db.session.commit()
    return redirect(f"/{user_id}/")

@app.route('/templates')
def show_templates():
    """See all published card templates"""
    templates = crud.get_published_templates()
    return render_template ("card_templates.html", templates = templates)

@app.route('/publish/<card_id>', methods=["POST"])
def publish_card(card_id):
    """publish card as template"""
    card = crud.get_card_by_id(card_id)
    card.published = True
    db.session.commit()
    return redirect("/templates")

@app.route('/savetemplate/<card_id>', methods=["POST"])
def save_template_as_card(card_id):
    """save template as user's new card"""
    if "user_id" in session:
        card = crud.get_card_by_id(card_id)
        title = card.title
        url = card.url
        published = False
        hidden = False
        user_id = session.get("user_id")
        user = crud.get_user_by_id(user_id)
        card = crud.create_card(title, url, published, hidden, user)
        
        db.session.add(card)
        db.session.commit()
        return redirect(f"/{user_id}")
    else:
        flash(Markup('Log in or create an account to create a card! <a href="/" class="alert-link">Go here.</a>'))
        return redirect("/templates")


@app.route('/sendcard/<card_id>')
def sendcard(card_id):
    """go to sendcard page"""
    card = crud.get_card_by_id(card_id)
    user_id = card.user_id
    contacts = crud.get_contacts_by_user(user_id)

    return render_template("send_card.html", card = card, contacts = contacts)

@app.route('/addressbook/<user_id>')
def show_addresses(user_id):
    """go to sendcard page"""

    contacts = crud.get_contacts_by_user(user_id)
    user = crud.get_user_by_id(user_id)


    return render_template("address_book.html", user=user, contacts = contacts)

@app.route("/addcontact", methods=["POST"])
def add_contact():
    """add contact to the user's address book"""
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    recipient = request.form.get("name")
    phone_number = request.form.get("phone_number")
    street_address = request.form.get("street_address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")
    hidden = False

    contact = crud.create_contact(recipient, str(phone_number), street_address, city, state, zipcode, hidden, user)
    db.session.add(contact)
    db.session.commit()
    return redirect(f"/addressbook/{user_id}")

@app.route("/add_sentcard/<card_id>", methods=["POST"])
def add_sentcard(card_id):
    """add sent card to database"""
    user_id = session.get("user_id")
    message = request.form.get("message")
    card = crud.get_card_by_id(card_id)
    contact_id = request.form.get("contact")
    contact = crud.get_contact_by_id(contact_id)
    today = datetime.today()
    date_sent = today.strftime("%Y-%m-%d %H:%M:%S")

    sms = client.messages.create(
                              body= message,
                              from_='+12056277820',
                              media_url=[card.url],
                              to='+1'+ contact.phone_number
                          )

    sentcard = crud.create_sentcard(message, date_sent, card, contact)
    db.session.add(sentcard)
    db.session.commit()
    return redirect(f"/{user_id}")

@app.route('/outbox/<user_id>')
def show_sentcards(user_id):
    """go to user's outbox"""
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    cards_sent = crud.get_sent_cards_by_user(user_id)
    cards = crud.get_cards_by_user(user_id)
    contacts = crud.get_contacts_by_user(user_id)
    
    return render_template("outbox.html", sent_cards = cards_sent, cards = cards, user=user, contacts=contacts)

@app.route("/hidecard/<card_id>", methods=["POST"])
def hide_card(card_id):
    "hide card from user"
    card = crud.get_card_by_id(card_id)
    card.hidden = True
    db.session.commit()
    user_id = session.get("user_id")

    return redirect(f"/{user_id}")

@app.route("/hidecontact/<contact_id>", methods=["POST"])
def hide_contact(contact_id):
    "hide contact from user"
    contact = crud.get_contact_by_id(contact_id)
    contact.hidden = True
    db.session.commit()
    user_id = session.get("user_id")

    return redirect(f"/addressbook/{user_id}")


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
