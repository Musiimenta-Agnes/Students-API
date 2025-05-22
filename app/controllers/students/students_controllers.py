
from app.extensions import bcrypt
from app.extensions import db
import validators
from app.models.students_model import Student
from flask import Blueprint, request,jsonify
from app.status_codes import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT


# Define the blueprint
student = Blueprint('student', __name__, url_prefix='/api/v1/student')

# Define the route
@student.route('/register', methods = ['POST'])
def register_student():
    data = request.json
    fName = data.get('fName')
    lName = data.get('lName')
    email = data.get('email')
    contact = data.get('contact')
    password = data.get('password')

    if not fName or not lName or not email or not password or not contact:
        return jsonify({
            'error': 'All fields are required!'
        }),HTTP_400_BAD_REQUEST
    

    if not validators.email(email):
         return jsonify({
            'error': 'Invalid email address!'
        }),HTTP_400_BAD_REQUEST
    
    if len(password) < 5:
         return jsonify({
            'error': 'Password is too short!'
        }),HTTP_400_BAD_REQUEST
    

    if Student.query.filter_by(email = email).first() is not None:
          return jsonify({
            'error': 'Email is already in use!'
        }),HTTP_409_CONFLICT
    
    if Student.query.filter_by(contact = contact).first() is not None:
          return jsonify({
            'error': 'Phone number is already in use!'
        }),HTTP_409_CONFLICT
    
    #Try hashing the password
    try:
         
         hashed_password = bcrypt.generate_password_hash(password)

         # Registe new data
         student_new_data = Student(fName=fName, lName=lName, email=email, password=hashed_password, contact=contact)

         # Adding the ne data to the database

         db.session.add(student_new_data)
         db.session.commit()

         # Getting the full names
         full_name = student_new_data.get_full_name()

         # The return message
         return jsonify({
              'message': full_name + 'has been successfully created as a student',
              'fName': student_new_data.fName,
              'lName': student_new_data.lName,
              'email': student_new_data.email,
              'password': student_new_data.password,
              'contact': student_new_data.contact
         }),HTTP_201_CREATED
         

    except Exception as e:
         return jsonify({
              'error': str(e)
         }),HTTP_500_INTERNAL_SERVER_ERROR
    


# Getting student by id
@student.route('/get/<int:id>', methods = ['GET'])
def get_student(id):
     try:
          
          student = Student.query.filter_by(id = id).first()
          if not student:
               return jsonify({
                    'error': 'That student des not exist!'
               }), HTTP_404_NOT_FOUND
          
          return jsonify ({
               'message': student.get_full_name() + 'has  been successfully retrieved',
               'fName': student.fName,
               'lName': student.lName,
               'email': student.email,
               'password': student.password,
               'contact': student.contact

          }),HTTP_200_OK



     except Exception as e:
          return jsonify ({
               'error': str(e)
          }),HTTP_500_INTERNAL_SERVER_ERROR
    


# Delete the student
@student.route('/delete/<int:id>', methods = ['DELETE'])
def delete_stuent(id):
     student = Student.query.filter_by(id = id).first()
     if not student:
          return jsonify ({'error': 'That student does not exist!'}),HTTP_404_NOT_FOUND
     else:
          db.session.delete(student)
          db.session.commit()

          return jsonify ({
               'message':  student.get_full_name() + ' has been successfully deleted'
          }),HTTP_200_OK

    

# Getting all the students
@student.route('/get', methods = ['GET'])
def get_all_students():
     try:
          all_students = Student.query.all()
          student_data = []

          for student in all_students:
               stdents_information = {
                'fName': student.fName,
               'lName': student.lName,
               'email': student.email,
               'password': student.password,
               'contact': student.contact
               }

               student_data.append(stdents_information)

          return jsonify({
                    'message': 'All students have neen retrieved',
                    'Total': len(student_data),
                    'Students': student_data
               }), HTTP_200_OK
          


     except Exception as e:
          return jsonify({
               'error': str(e)
          }),HTTP_500_INTERNAL_SERVER_ERROR
     

# Updatting students details
@student.route('/edit/<int:id>', methods = ['PUT', 'PATCH'])
def update_student(id):
     try:
          student = Student.query.filter_by(id = id).first()
          if not student:
               return jsonify({
                    'error':'That student does not exist!'
               }),HTTP_404_NOT_FOUND
          
          else:
               fName = request.get_json().get('fName',student.fName)
               lName = request.get_json().get('lName',student.lName)
               email = request.get_json().get('email',student.email)
               password = request.get_json().get('password',student.password)
               contact = request.get_json().get('contact',student.contact)


               #Update the details
               student.fName = fName 
               student.lName = lName 
               student.email = email 
               student.password = password 
               student.contact = contact 

               # Commit
               db.session.commit()

               # The return message

               return jsonify({
                    'message': fName + lName +  'has been successifully updated',
                    'fName': student.fName,
                    'lName': student.lName,
                    'email': student.email,
                    'password': student.password,
                    'contact': student.contact
               }),HTTP_200_OK

     except Exception as e:
          
          return jsonify({
               'error':str(e)
          }),HTTP_500_INTERNAL_SERVER_ERROR