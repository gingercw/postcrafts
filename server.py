"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, Markup)

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from twilio.rest import Client

from model import connect_to_db, db

from datetime import datetime

import sched, time

import crud 

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

from jinja2 import StrictUndefined

import os

import requests



app = Flask(__name__)
app.secret_key = "APIKEY"
app.jinja_env.undefined = StrictUndefined

CLIENTID = os.environ['CLIENTID']
CLOUDINARY_URL = os.environ['CLOUDINARY_URL']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

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
        return render_template("index.html")


@app.route('/<user_id>/new_card')
def make_card(user_id):
    """create a new card"""
    user = crud.get_user_by_id(user_id)
    return render_template("new_card.html", user=user)

@app.route('/edit_card/<card_id>')
def edit_card(card_id):
    """render template for edit card"""
    card = crud.get_card_by_id(card_id)
    card_id = card.card_id
    return render_template("edit_card.html")

@app.route('/edit_card/details/<card_id>')
def edit_card_details(card_id):
    """pass card details to edit card page"""
    card = crud.get_card_by_id(card_id)
    card_id = card.card_id
    card_url = card.url
    user_id = session.get("user_id")
    return jsonify({
       "card_id": card_id,
       "card_url": card_url,
       "user_id": user_id
    })


@app.route('/save_edits', methods=["POST"])
def save_edits():
    """update url to card to save changes"""
    card_id = request.json.get("card_id")
    print(card_id)
    card = crud.get_card_by_id(card_id)
    raw_image = request.json.get("rawImage")
    upload_result = upload(raw_image)
    url, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=600, height=400)
    card.url = url
    print(card.url)
    user_id = session.get("user_id")
    print(user_id)
    db.session.commit()
    return redirect(f"/{user_id}/")


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
    """Find 8 photos from Unsplash with query term."""
    photo_query = request.args.get("photo_query")
    headers_dict = {"Authorization": f"Client-ID {CLIENTID}"}

    url = f'https://api.unsplash.com/photos/random?query={photo_query}&orientation=landscape&count=8'

    response = requests.get(url, headers=headers_dict)

    return response.text


@app.route('/save', methods=["POST"])
def save_card():
    """save card to database"""
    title = request.json.get("title")
    raw_image = request.json.get("rawImage")
    upload_result = upload(raw_image)
    url, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=600, height=400)
    published = False
    tags = None
    hidden = False
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    card = crud.create_card(title, url, published, tags, hidden, user)
    
    db.session.add(card)
    db.session.commit()
    return redirect(f"/{user_id}/")


@app.route('/templates')
def search_templates():
    """search templates using keywords"""
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    keyword = request.args.get("template_search")
    if keyword is None:
        templates = crud.get_published_templates()
    else:
        templates = crud.filter_templates(keyword)
    return render_template ("card_templates.html", templates = templates, user = user)


@app.route('/publish/<card_id>', methods=["POST"])
def publish_card(card_id):
    """publish card as template"""
    card = crud.get_card_by_id(card_id)
    
    if card.published is True:
        flash("This card is already a template!")
        user_id = session.get("user_id")
        return redirect(f"/{user_id}")
    else:
        card.published = True
        keywords = request.form.get("keywords")
        card.tags = keywords
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
        tags = None
        hidden = False
        user_id = session.get("user_id")
        user = crud.get_user_by_id(user_id)
        card = crud.create_card(title, url, published, tags, hidden, user)
        
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
    user = crud.get_user_by_id(user_id)
    contacts = crud.get_contacts_by_user(user_id)

    return render_template("send_card.html", card = card, contacts = contacts, 
    user = user)



@app.route('/addressbook/<user_id>')
def show_addresses(user_id):
    """go to addressbook"""
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
    email = request.form.get("email")
    hidden = False

    contact = crud.create_contact(recipient, str(phone_number), email, hidden, user)
    db.session.add(contact)
    db.session.commit()
    return redirect(f"/addressbook/{user_id}")

@app.route("/add_sentcard/<card_id>", methods=["POST"])
def add_sentcard(card_id):
    """add sent card to database"""
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    message = request.form.get("message")
    card = crud.get_card_by_id(card_id)
    contact_id = request.form.get("contact")
    medium = request.form.get("medium")
    contact = crud.get_contact_by_id(contact_id)
    today = datetime.today()
    date_sent = today.strftime("%Y-%m-%d %H:%M:%S")

    if medium == "text":
        sms = client.messages.create(
                                body= message,
                                from_='+12056277820',
                                media_url=[card.url],
                                to='+1'+ contact.phone_number
                            )
    else:      

        sender = "postcraftcards@gmail.com"
        receiver = contact.email
        # Create the root message 

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = f'A Card for {contact.recipient}!'
        msgRoot['From'] = sender
        msgRoot['To'] = receiver

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(message)
        msgAlternative.attach(msgText)

        msgText = MIMEText(f'{message}<br><img src={card.url}>', 'html')
        msgAlternative.attach(msgText)

        smtp = smtplib.SMTP()
        smtp.connect(host='smtp.sendgrid.net', port=587) #SMTp Server Details
        smtp.login("apikey", EMAIL_PASSWORD) #Username and Password of Account
        smtp.sendmail(sender, receiver, msgRoot.as_string())
        smtp.quit()

    sentcard = crud.create_sentcard(message, date_sent, card, contact)
    db.session.add(sentcard)
    db.session.commit()
    return redirect(f"/outbox/{user_id}")

# @app.route('/schedule/<card_id>')
# def schedule_card(card_id):
#     """schedule card for delivery"""
#     card = crud.get_card_by_id(card_id)
#     date = request.args.get("date")
#     time = request.args.get("time")
#     s = sched.scheduler(time.time, time.sleep)
#     s.enterabs(datetime(2018, 1, 1, 12, 20, 59, 0).timestamp(), 1, add_sentcard,argument=)
#     s.enterabs(datetime(2018, 1, 1, 12, 20, 59, 500000).timestamp(), 1, func)
#     s.run()

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
