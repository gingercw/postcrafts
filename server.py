"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)

from model import connect_to_db, db

import crud 

from jinja2 import StrictUndefined

import os

import requests

app = Flask(__name__)
app.secret_key = "APIKEY"
app.jinja_env.undefined = StrictUndefined

CLIENTID = os.environ['CLIENTID']

@app.route('/')
def index():
    """go to homepage"""
    return render_template("homepage.html")

@app.route('/new_card')
def make_card():
    """create a new card"""
    return render_template("new_card.html")


@app.route('/card_templates')
def get_card_templates():
    """show all published card templates"""
    return render_template("card_templates.html")

@app.route('/<user_id>')
def get_user_details(user_id):
    """show user profile page with created cards"""
    user_details = crud.get_user_by_id(user_id)
    users_cards = crud.get_cards_by_user(user_id)
    cards_sent = crud.get_sent_cards_by_user(user_id)
    addresses = crud.get_addresses_by_user(user_id)


    return render_template("user_profile.html", user = user_details, cards = users_cards, sent_cards = cards_sent, addresses = addresses)

@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""
    user_email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    street_address = request.form.get("street_address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")

    email_check = crud.get_user_by_email(user_email)

    if email_check is None:
        new_user = crud.create_user(user_email, password, name, street_address, city, state, zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("Whoo hoo! Log in to start creating.")
    else:
        flash("An account already exists with that email address. Try signing up again with a different email.")
    return redirect("/")
    
    

@app.route("/login", methods=["POST"])
def login():
    """log in existing user"""
    input_email = request.form.get("email")
    input_password = request.form.get("password")

    user_info = crud.get_user_by_email(input_email)

    if input_password == user_info.password:
        user_id = user_info.user_id
        session["user_id"] = user_id
        return redirect(f"/{user_id}")
        
@app.route('/photos')
def get_photos():
    """View the details of an event."""
    place = request.args.get("location")
    headers_dict = {"Authorization": f"Client-ID {CLIENTID}"}

    url = f'https://api.unsplash.com/photos/random?query={place}&orientation=landscape&count=8'

    response = requests.get(url, headers=headers_dict)

    return response.text

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

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
