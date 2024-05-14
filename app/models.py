from email.policy import default
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    # is_admin = db.Column(db.Boolean, nullable=False, default=0)
    
    # Load thông tin user thông qua đối tượng userMixin
    @login.user_loader
    def load_user(id):
        if id.startswith('users'):
            return User.query.filter_by(id=int(id)).first()
        else:
            return Parent.query.get(int(id))
    
    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)


    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)


class Class(db.Model):
    __tablename__ = "classes"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    teachers = db.relationship("Teacher", backref="class")
    meals = db.relationship("Meal", backref="class")
    students = db.relationship("Student", backref="class")
    works = db.relationship("Work", backref="class")
    
    

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    degree = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)  
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    class_id= db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    
 
class Meal(db.Model):
    __tablename__ = "meals"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)   
    time = db.Column(db.Date, nullable=False)
    dishs = db.relationship("Dish", backref="meal")
    class_id= db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    
    
class Dish(db.Model):
    __tablename__ = "dishes"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)   
    meal_id= db.Column(db.Integer, db.ForeignKey("meals.id"), nullable=False)
    

class Work(db.Model):
    __tablename__ = "works"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)   
    teacher_name = db.Column(db.String, nullable=False)   
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    class_id= db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    
    
class Student(db.Model):
    __tablename__ = "students"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)     
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)  
    healths = db.relationship("Health", backref="student")   
    parents = db.relationship("Parent", backref="student") 
    tuitions = db.relationship("Tuition", backref="student")
    class_id= db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    

class Health(db.Model):
    __tablename__ = "healths"   
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    height = db.Column(db.String, nullable=False)    
    weight = db.Column(db.String, nullable=False)  
    note = db.Column(db.String, nullable=False)  
    student_id= db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    
    
class Tuition(db.Model):
    __tablename__ = "tuitions"   
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False)
    tuition_receivable = db.Column(db.Integer, nullable=False)
    tuition_paid = db.Column(db.Integer, nullable=False) 
    tuition_debt = db.Column(db.Integer, nullable=False)
    pays = db.relationship("Pay", backref="tuition")
    student_id= db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    

class Parent(UserMixin, db.Model):
    __tablename__ = "parents"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    phone = db.Column(db.String, nullable=False, unique=True) 
    username = db.Column(db.String, nullable=False) 
    password = db.Column(db.String, nullable=False) 
    # pays = db.relationship("Pay", backref="parent")
    # notifications = db.relationship("Notification", backref="parent")
    student_id= db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    

    @login.user_loader
    def load_parent(id):
        if id.startswith('parents'):
            return Parent.query.filter_by(id=int(id)).first()
        else:
            return User.query.get(int(id))
        
    
    
    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)


    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    
    
class Pay(db.Model):
    __tablename__ = "pays"   
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    money = db.Column(db.Integer, nullable=False) 
    payer = db.Column(db.String, nullable=False) 
    # parent_id= db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=False)
    tuition_id= db.Column(db.Integer, db.ForeignKey("tuitions.id"), nullable=False)


class Notification(db.Model):
    __tablename__ = "notifications"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) 
    content = db.Column(db.String, nullable=False) 
    time = db.Column(db.DateTime, default=datetime.now)


    
    
