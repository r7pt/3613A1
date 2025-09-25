from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Intern(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    title = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.String(500),nullable=True)

    user =db.relationship('User',backref=db.backref('shortlists',lazy=True))
    
    def __init__(self,user_id,title,description):
        self.user_id=user_id
        self.title=title
        self.description=description
    
    def __repr__(self):
        return f'Shortlist {self.id}-{self.user_id}-{self.title}-{self.description}'