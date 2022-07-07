"""CRUD operations."""

from model import db, User, Card, Contact, SentCard, connect_to_db


# Functions start here!

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_user_by_id(user_id):
    """returns user's id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """return user with the email"""
    return User.query.filter(User.email == email).first()


def create_card(title, url, published, tags, hidden, user):
    """Create and return a new card."""

    card = Card(title=title, url=url, published=published, tags=tags, hidden=hidden, user=user)

    return card

def get_card_by_id(card_id):
    """returns all cards from a user"""
    return Card.query.get(card_id)

def get_cards_by_user(user_id):
    """returns all cards from a user"""
    return Card.query.filter_by(user_id = user_id, hidden = False).order_by(Card.card_id.desc()).all()

def get_published_templates():
    """shows all cards that were published"""
    return Card.query.filter_by(published = True).order_by(Card.card_id.desc())


def filter_templates(term):
    """return templates with similar keywords"""
    return db.session.query(Card).filter(db.and_(Card.published == True, Card.tags.ilike(f"%{term}%"))).all()

def create_contact(recipient, phone_number, email, hidden, user):
    """Create and return a new contact."""
    contact = Contact(recipient=recipient, phone_number=phone_number, email=email, hidden=hidden, user=user)

    return contact

def get_contacts_by_user(user_id):
    """returns all contacts for a user"""
    return Contact.query.filter_by(user_id = user_id, hidden = False).order_by(Contact.contact_id.desc()).all()

def get_contact_by_id(contact_id):
    """returns a contact through contact id"""
    return Contact.query.get(contact_id)

def create_sentcard(message, date_sent, card, contact):
    """Record card that was sent."""
    sentcard = SentCard(message=message, date_sent=date_sent, card=card, contact=contact)

    return sentcard


def get_sent_cards_by_user(user_id):
    """returns all sent cards from a user"""
    return db.session.query(SentCard).join(Card).filter(Card.user_id == user_id).order_by(SentCard.date_sent.desc()).all()
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)