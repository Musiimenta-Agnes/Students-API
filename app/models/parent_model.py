from app.extensions import db

class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, nullable = False, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email= db.Column(db.String(255), nullable = False, unique = True)
    contact= db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)


    def __init__(self, name,email, contact,password):
        self.name = name
        self.email = email
        self.contact = contact
        self.password = password


    def get_full_name(self):
        return f"{self.name}"
        
