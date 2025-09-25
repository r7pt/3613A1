from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .shortlist import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'User {self.id}-{self.username}'
    
    def create_intern(self,title,description):
        from .intern import Intern
        new_intern = Intern(user_id=self.id,title=title,description=description)
        db.session.add(new_intern)
        db.session.commit()
        return new_intern
       
    
    def review_app(self,response,shortlist):
        application = Shortlist.query.filter_by(id=shortlist.id).first()
        application.response=response
        db.session.add(application)
        db.session.commit()
        return application
