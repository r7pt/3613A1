from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(120),nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }
    
    def __repr__(self):
        return f'Staff {self.id}-{self.username}'

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def add_intern(self,intern_id,student_id):
        from .shortlist import Shortlist
        applcation = Shortlist(intern_id=intern_id,student_id=student_id,staff_id=self.id)
        db.session.add(applcation)
        db.session.commit()
        return applcation
    
