from app.extensions import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key = True)
    fName =  db.Column(db.String(255), nullable = False)
    lName =  db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    contact = db.Column(db.String(255), nullable = False)


    def __init__(self,fName,lName,email,password,contact):
         self.fName = fName
         self.lName = lName
         self.email = email 
         self.password = password
         self.contact = contact



    def get_full_name(self):
         return f"{self.fName} {self.lName}"
         
              
        