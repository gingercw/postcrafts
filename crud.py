"""CRUD operations."""

from model import db, User, Card, Address, SentCard, connect_to_db


# Functions start here!

def create_user(email, password, name, street_address, city, state, zipcode):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name, street_address=street_address, city=city, state=state, zipcode=zipcode)

    return user

def get_user_by_id(user_id):
    """returns user's id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """return user with the email"""
    return User.query.filter(User.email == email).first()

def get_user_by_card(card_id):
    """return user with the card id"""
    return User.query.filter(User.email == email).first()
    return db.session.query(User).join(Card).filter(Card.user_id == user_id).first()


def create_card(title, url, published, user):
    """Create and return a new card."""

    card = Card(title=title, url=url, published=published, user=user)

    return card

def get_card_by_id(card_id):
    """returns all cards from a user"""
    return Card.query.get(card_id)

def get_cards_by_user(user_id):
    """returns all cards from a user"""
    return Card.query.filter_by(user_id = user_id).all()

def get_published_templates():
    """shows all cards that were published"""
    return Card.query.filter_by(published = True).all()

def create_address(recipient, street_address, city, state, zipcode, user):
    """Create and return a new address."""

    address = Address(recipient=recipient, street_address=street_address, city=city, state=state, zipcode=zipcode, user=user)

    return address

def get_addresses_by_user(user_id):
    """returns all cards from a user"""
    return Address.query.filter_by(user_id = user_id).all()

def create_sentcard(message, date_sent, card, address):
    """Create and return a new address."""

    sentcard = SentCard(message=message, date_sent=date_sent, card=card, address=address)

    return sentcard

def get_sent_cards_by_user(user_id):
    """returns all cards from a user"""
    return db.session.query(SentCard).join(Card).filter(Card.user_id == user_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)