from app.extensions import db,bcrypt
from flask import Blueprint,request,jsonify
import validators
from app.models.parent_model import Parent
from app.status_codes import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_409_CONFLICT

# Registering a parent
parent = Blueprint('parent', __name__,url_prefix='/api/v1/parent')
@parent.route('/register', methods = ['POST'])
def register_parent():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    contact = data.get('contact')

 
 # Checking for all fileds
    if not name or not email or not password or not contact:
        return jsonify({
            'error': 'All fields are required!'
        }),HTTP_400_BAD_REQUEST
    
    # Email verification
    if not validators.email(email):
        return jsonify({
            'error': 'Invalid email!!'
        }),HTTP_400_BAD_REQUEST
    
    if len(password) < 5:
        return jsonify({
            'error': 'Password is too short!'
        }),HTTP_400_BAD_REQUEST
    

    # Checking for dat consistency
    if Parent.query.filter_by(email = email).first():
        return jsonify({
            'error': 'Email is already in use!'
        }),HTTP_409_CONFLICT
    

    if Parent.query.filter_by(contact = contact).first():
        return jsonify({
            'error': 'Phone number is already in use!'
        }),HTTP_409_CONFLICT
    

    # Try hashing the assword

    try:
        hashed_password = bcrypt.generate_password_hash(password)

        # New parent data
        new_data = Parent(name=name,email=email,password=hashed_password,contact=contact)

        # Getting full parent name
        full_name = new_data.get_full_name()

        # Adding the parent data to the databases
        db.session.add(new_data)
        db.session.commit()

        # The return message
        return jsonify({
            'message': full_name + 'has been sccessfully registered',
            'name': new_data.name,
            'email': new_data.email,
            'password': new_data.password,
            'contact': new_data.contact

        }),HTTP_200_OK


    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
    

# Getting parent by id
@parent.route('/get/<int:id>', methods = ['GET'])
def get_parent(id):
    parent = Parent.query.filter_by(id = id).first()

    if not parent:
        return jsonify({
            'error': 'This parent does not exist!'
        }),HTTP_404_NOT_FOUND
    
    else:
        return jsonify({
            'message': parent.name + 'has been sccessfully retrieved',
            'name': parent.name,
            'email': parent.email,
            'password': parent.password,
            'contact': parent.contact
        }),HTTP_200_OK
    

# Deleting the parents details
@parent.route('/delete/<int:id>', methods = ['DELETE'])
def delete_parent(id):
    parent = Parent.query.filter_by(id = id).first()

    if not parent:
        return jsonify({
            'error': 'This parent does not exist!'
        }),HTTP_404_NOT_FOUND
    
    else:
        db.session.delete(parent)
        db.session.commit()

        return jsonify({
            'message': parent.name + 'has been sccessfully deleted',
         
        }),HTTP_200_OK
    


    #Getting all te parents details
@parent.route('/get', methods = ['GET'])
def getting_all_parents():
    all_parents = Parent.query.all()
    parent_data = []

    for parent in all_parents:
        parent_information = {
            'name': parent.name,
            'email': parent.email,
            'password': parent.password,
            'contact': parent.contact
        }

        parent_data.append(parent_information)

    return jsonify({
            'message': "All parents have been successifully retrieved",
            'Total': len(parent_data),
            'Parents': parent_data
        }),HTTP_200_OK




    # Updating the parent details

@parent.route('/edit/<int:id>', methods = ['PUT', 'PATCH'])
def update_parent(id):
    parent = Parent.query.filter_by(id = id).first()

    if not parent:
        return jsonify({
            'error': 'This parent does not exist!'
        }),HTTP_404_NOT_FOUND
    
    else:
        name = request.get_json().get('name', parent.name)
        email = request.get_json().get('email', parent.email)
        password = request.get_json().get('password', parent.password)
        contact = request.get_json().get('contact', parent.contact)


        # Updating the data
        parent.name = name
        parent.email = email
        parent.password = password
        parent.contact = contact

        # Commit the updated data
        db.session.commit()

        #The return message
        return jsonify({
            'message': parent.name + 'has been sccessfully updated',
            'name': parent.name,
            'email': parent.email,
            'password': parent.password,
            'contact': parent.contact

        }),HTTP_200_OK

