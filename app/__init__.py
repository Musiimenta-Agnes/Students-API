from flask import Flask
from app.extensions import db,migrate
from app.controllers.teachers.teachers_controller import teacher
from app.controllers.students.students_controllers import student
from app.controllers.parents.parent_controller import parent



def create_app():

    app = Flask(__name__)
    app.config.from_object('config:Config')
    db.init_app(app)
    migrate.init_app(app,db)

    # Register models
    from app.models.students_model import Student
    from app.models.teachers_model import Teacher
    from app.models.parent_model import Parent


   # Register the blue prints
    app.register_blueprint(teacher)
    app.register_blueprint(student)
    app.register_blueprint(parent)
   


    @app.route('/')
    def index():
        return "Student Managemant Application"


    return app