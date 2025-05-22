
from flask import Blueprint
from flask import request,jsonify
from app.extensions import bcrypt,db
from app.models.teachers_model import Teacher
import validators
from app.status_codes import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT


teacher = Blueprint('teacher', __name__, url_prefix='/api/v1/teacher')
@teacher.route('/register', methods = ['POST'])
def register_teacher():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    contact = data.get('contact')
    password = data.get('password')


    # Avoiding redanduncy
    if not name or not  email or not contact:
        return jsonify({
            'error': 'All field are required'
        }), HTTP_400_BAD_REQUEST
    
    # Validating the email
    if not validators.email(email):
        return jsonify({
            'error': 'Invalid email'
        }), HTTP_400_BAD_REQUEST
    
    # Checking the length of password
    if len(password) < 5:
        return jsonify({
            'error': 'Password too short!'
        }), HTTP_400_BAD_REQUEST
    
    # Checking for data nconsisency
    if Teacher.query.filter_by(email = email).first() is not None:
        return jsonify({
            'error': 'Email already in use'
        }), HTTP_409_CONFLICT
    
    if Teacher.query.filter_by(contact = contact).first() is not None:
        return jsonify({
            'error': 'Phone number is already in use'
        }), HTTP_409_CONFLICT

    
    # Hashing our password
    try:

        hashed_password = bcrypt.generate_password_hash(password)

         # New data
        teacher_new_data = Teacher(name=name, email=email,contact=contact,password=hashed_password)

        # Adding and registering the new data
        db.session.add(teacher_new_data)
        db.session.commit()

        # Generating full name
        full_name = teacher_new_data.get_name()

        # Message to return after the request

        return jsonify({
             'message': 'Teacher' + ' ' + full_name + ' ' +'has been successfully registered',
             'name': teacher_new_data.name,
             'email': teacher_new_data.email,
             'contact': teacher_new_data.contact,
             'password': teacher_new_data.password
        }),HTTP_201_CREATED



    except Exception as e:
            return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    
   


# Getting teacher by id

@teacher.route('/get/<int:id>',methods = ['GET'])
def get_teacher(id):
     try:
          teacher = Teacher.query.filter_by(id = id).first()
          if not teacher:
               return jsonify ({'error': 'That teacher does not exist!'}),HTTP_404_NOT_FOUND
          
          return jsonify({
               'message': teacher.get_name() + ' has been successfully retrieved',
               'name': teacher.name,
               'email': teacher.email,
               'contact': teacher.contact,
               'password': teacher.password

          }), HTTP_200_OK
          


     except Exception as e:
          return jsonify({
               'error': str(e)
          }),HTTP_500_INTERNAL_SERVER_ERROR

    
# Deleting the teacher by id
@teacher.route('/delete/<int:id>', methods = ['DELETE'])
def delete_teacher(id):
     teacher = Teacher.query.filter_by(id = id).first()
     if not teacher:
          return jsonify ({'error': 'That teacher does not exist!'}),HTTP_404_NOT_FOUND
     else:
          db.session.delete(teacher)
          db.session.commit()

          return jsonify ({
               'message': 'Teacher' + teacher.get_name() + ' has been successfully deleted'
          }),HTTP_200_OK
          


# Getting all the teachers information
@teacher.route('/get', methods = ['GET'])
def get_all_teachers():
     try:
          all_teachers = Teacher.query.all()
          teachers_data = []

          for teacher in all_teachers:
               teachers_information = {
                   'name': teacher.name,
                   'email': teacher.email,
                   'contact': teacher.contact,
                   'password': teacher.password
                    
               }
               teachers_data.append(teachers_information)
          return jsonify({
               'message':'All teachers have been successifully retrieved',
               'Total': len(teachers_data),
               'Teachers': teachers_data
                    
               }),HTTP_200_OK
          

     except Exception as e:
          return jsonify ({
               'error': str(e)
          }),HTTP_500_INTERNAL_SERVER_ERROR
     



# Updating the teachers details
@teacher.route('/edit/<int:id>', methods = ['PUT', 'PATCH'])
def update_teacher(id):
     teacher = Teacher.query.filter_by(id = id).first()

     if not teacher:
          return jsonify({'error': 'That teacher does not exixt!'}),HTTP_404_NOT_FOUND
     
     else:
          name = request.get_json().get('name',teacher.name)
          email = request.get_json().get('email',teacher.email)
          password = request.get_json().get('password',teacher.password)
          contact = request.get_json().get('contact',teacher.contact)


        # Update the details
          teacher.name = name
          teacher.email = email
          teacher.password = password
          teacher.contact = contact

        # Commit the updates
          db.session.commit()

        # The return message
          return jsonify({
                   'message': name + 'has been successifully updated',
                   'name': teacher.name,
                   'email': teacher.email,
                   'contact': teacher.contact,
                   'password': teacher.password

          }),HTTP_200_OK
         
