from app.extensions import db

class Teacher(db.Model):
       __tablename__ = 'Teachers'

       id = db.Column(db.Integer, nullable = False, primary_key = True)
       name = db.Column(db.String(255), nullable = False)
       email= db.Column(db.String(255), nullable = False, unique = True)
       contact= db.Column(db.String(255), nullable = False, unique = True)
       password = db.Column(db.String(255), nullable = False)



       def __init__(self, name, email, contact, password):
              self.name = name 
              self.email =  email
              self.contact = contact
              self.password = password



       def get_name(self):
              return self.name
       