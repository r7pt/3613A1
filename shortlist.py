from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Shortlist(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    intern_id = db.Column(db.Integer,db.ForeignKey('intern.id'),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    staff_id=db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=False,)
    response=db.Column(db.String(15),nullable=False,default='pending')

    intern =db.relationship('Intern',backref=db.backref('shortlists',lazy=True))
    staff = db.relationship('Staff',backref=db.backref('shortlists', lazy =True))
    student=db.relationship('Student',backref=db.backref('shortlists',lazy=True))

    def __init__(self,intern_id,student_id,staff_id,response='pending'):
        self.intern_id=intern_id
        self.student_id=student_id
        self.staff_id=staff_id
        self.response=response

    def respond(self,respond):
        self.respond=respond
        db.session.add(self)
        db.session.commit()     
        

    def __repr__(self):
        return f'Shortlist {self.id}-{self.intern_id}-{self.staff}-{self.student_id}-{self.response}'
