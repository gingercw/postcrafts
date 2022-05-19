"""Models for card maker app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    email = db.Column(db.String, unique = True,)
    password = db.Column(db.String)
    name = db.Column(db.String, nullable = True)
    street_address = db.Column(db.String, nullable = True)
    city = db.Column(db.String, nullable = True)
    state = db.Column(db.String, nullable = True)
    zipcode = db.Column(db.Integer, nullable = True)
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

        
class Card(db.Model):
    """A card made by a user."""

    __tablename__ = 'cards'

    card_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    title = db.Column(db.String)
    # location = db.Column(db.String) #the place a postcard represents e.g. New York, San Franciso, etc.
    url = db.Column(db.String)
    published = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref="cards")


    def __repr__(self):
        return f'<Card card_id={self.card_id} title={self.title}>'


class Address(db.Model):
    """Address the user sends cards to."""

    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    recipient = db.Column(db.String)
    street_address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    
    user = db.relationship("User", backref="addresses")

    def __repr__(self):
        return f'<Address address_id={self.address_id} recipient={self.recipient}>'

class SentCard(db.Model):
    """Address the user sends cards to."""

    __tablename__ = 'sent_cards'

    sent_card_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    message = db.Column(db.Text)
    date_sent = db.Column(db.DateTime)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.card_id"))
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.address_id"))
    
    card = db.relationship("Card", backref="sent_cards")
    address = db.relationship("Address", backref="sent_cards")

    def __repr__(self):
        return f'<SentCard sentcard_id={self.sentcard_id} date_sent={self.date_sent}>'





def connect_to_db(flask_app, db_uri="postgresql:///cards", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
