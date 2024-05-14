from flask import jsonify
from email import message
from turtle import title
from flask import render_template, request, flash, redirect, url_for
from app import app
from app.models import *
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import and_
from sqlalchemy import or_
import os
from werkzeug.utils import secure_filename


@app.route("/")
def index():
    return render_template ("index.html")


## -------------- Quản lý lớp học----------------------- ##
@app.route("/class_management")
@login_required
def class_management():
    classes = Class.query.all()
    return render_template ("class_management.html", classes=classes)


@app.route("/addNewClass_s1")
@login_required
def addNewClass_s1():
    return render_template ("addNewClass_s1.html")


@app.route("/addNewClass_s2", methods=["POST"])
@login_required
def addNewClass_s2():
    try: 
        name = request.form.get("name")
        class1 = Class(name=name)
        db.session.add(class1)
        db.session.commit()
        flash(f'Thêm mới thành công lớp: {name}')
        return redirect(url_for('class_management'))   
    except: 
        flash(f'Tên lớp học đã tồn tại')
        return redirect(url_for('class_management'))


@app.route("/update_class/<int:class_id>")
@login_required
def update_class(class_id):
    classes = Class.query.get(class_id)
    return render_template ("update_class_s1.html", classes=classes)


@app.route("/update_class_s2", methods=["POST"])
@login_required
def update_class_s2():
    try:
        class_id = request.form.get("id")
        name = request.form.get("name")
        class2= Class.query.get(class_id)
        class2.name = name
        db.session.commit()
        flash(f'Cập nhật thành công lớp: {name}')
        return redirect(url_for('class_management'))
    except: 
        flash(f'Tên lớp học đã tồn tại')
        return redirect(url_for('class_management'))



@app.route("/delete_class/<int:class_id>")
@login_required
def delete_class(class_id):
    try:
        class1 = Class.query.get(class_id)
        name = class1.name
        db.session.delete(class1)
        db.session.commit()
        flash(f'Đã xóa thành công lớp: {name}')
        return redirect(url_for('class_management'))
    except:
        flash(f'Bạn cần xóa các thông tin về học sinh, giáo viên, bữa ăn và hoạt động liên quan trước khi xóa bỏ lớp học này')
        return redirect(url_for('class_management'))


##------------------Quản lý học sinh-----------------------##


@app.route("/student_management")
@login_required
def student_management():
    students = Student.query.all()
    class1 = Class.query.all()
    return render_template ("student_management.html", students=students, class1=class1)


@app.route("/student_management_s2/<int:class_id>", methods=["GET", "POST"])
@login_required
def student_management_s2(class_id):
    students = Student.query.filter(Student.class_id == class_id)
    class1 = Class.query.all()
    return render_template ("student_management.html", students=students, class1=class1)


@app.route("/addNewStudent_s1")
@login_required
def addNewStudent_s1():
    class1 = Class.query.all()
    return render_template ("addNewStudent_s1.html", class1=class1)


@app.route("/addNewStudent_s2/<int:class_id>")
@login_required
def addNewStudent_s2(class_id):
    class1 = Class.query.get(class_id)
    return render_template("addNewStudent_s2.html", class1=class1)


@app.route("/addNewStudent_s3", methods=["POST"])
@login_required
def addNewStudent_s3():  
    #Get form information
    class_id = int(request.form.get("class_id"))
    name = request.form.get("name")
    gender = request.form.get("gender")
    date_of_birth= request.form.get("date_of_birth")
    address= request.form.get("address")
    student = Student(name=name, gender=gender, date_of_birth=date_of_birth, address=address, class_id=class_id)
    db.session.add(student)
    db.session.commit()
    flash(f'Đã thêm thành công học sinh: {name}')
    return redirect(url_for('student_management'))


      
@app.route("/searchStudentForMagagement", methods=["GET","POST"])
@login_required
def searchStudentForMagagement():
    id = request.args.get("id")
    student = Student.query.get(id)
    class1 = Class.query.all()
    return render_template ("selectStudentForManagement.html", student=student, class1=class1)



@app.route("/update_student/<int:student_id>")
@login_required
def update_student(student_id):
    student = Student.query.get(student_id)
    return render_template ("update_student_s1.html", student=student)


@app.route("/update_student_s2", methods=["POST"])
@login_required
def update_student_s2():
    try:
        id = request.form.get("id")
        name = request.form.get("name")
        gender = request.form.get("gender")
        date_of_birth= request.form.get("date_of_birth")
        address= request.form.get("address")
        student= Student.query.get(id)
        student.name = name
        student.gender = gender
        student.date_of_birth = date_of_birth
        student.address = address
        db.session.commit()
        flash(f'Cập nhật thành công thông tin học sinh: {name}')
        return redirect(url_for('student_management'))
    except:
            flash(f'Vui lòng điền đầy đủ thông tin')
            return redirect(url_for('student_management'))
   


@app.route("/delete_student/<int:student_id>")
@login_required
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        name = student.name
        db.session.delete(student)
        db.session.commit()
        flash(f'Đã xóa thành công học sinh: {name}')
        return redirect(url_for('student_management'))
    except:
            flash(f'Bạn cần xóa thông tin phụ huynh, sức khỏe và học phí liên quan trước khi xóa học sinh này')
            return redirect(url_for('student_management'))


#----------------------Quản lý thông tin phụ huynh--------------------

@app.route("/parent_management_s1/<int:student_id>")
@login_required
def parent_management_s1(student_id):
    # dùng filter thay vì get để lấy nhiều phụ huynh thay vì 1 người
    parents = Parent.query.filter(Parent.student_id == student_id)
    return render_template ("parent_management.html", parents=parents)


@app.route("/parent_management")
@login_required
def parent_management():
    parents = Parent.query.all()
    return render_template ("parent_management.html", parents=parents)


@app.route("/addNewParent_s1")
@login_required
def addNewParent_s1():
    students = Student.query.all()
    return render_template ("addNewParent_s1.html", students=students)


# Tìm kiếm học sinh để thêm phụ huynh

@app.route("/searchStudent", methods=["GET","POST"])
@login_required
def searchStudent():
    id = request.args.get("id")
    student = Student.query.get(id)
    return render_template ("selectStudent.html", student=student)
      

# Thêm mới phụ huynh theo id học sinh đang xem
@app.route("/addNewParent_s2/<int:student_id>")
@login_required
def addNewParent_s2(student_id):
    student = Student.query.get(student_id)
    return render_template("addNewParent_s2.html", student=student)


@app.route("/addNewParent_s3", methods=["POST"])
@login_required
def addNewParent_s3():  
    #Get form information
    try:
        student_id = int(request.form.get("student_id"))
        name = request.form.get("name")
        phone = request.form.get("phone")
        username= request.form.get("username")
        password= request.form.get("password")
        parent = Parent(name=name, phone=phone, username=username, password=password, student_id=student_id)
        parent.set_password(request.form.get("password"))
        db.session.add(parent)
        db.session.commit()
        flash(f'Đã thêm thành công phụ huynh: {name}')
        return redirect(url_for('parent_management'))
    except:
        flash(f'Số điện thoại này đã tồn tại')
        return redirect(url_for('parent_management'))
         


# -----Cập nhật thông tin phụ huynh----------------------


@app.route("/update_parent/<int:parent_id>")
@login_required
def update_parent(parent_id):
    parent = Parent.query.get(parent_id)
    return render_template ("update_parent_s1.html", parent=parent)


@app.route("/update_parent_s1", methods=["POST"])
@login_required
def update_parent_s1():
    try:
        parent_id = request.form.get("parent_id")
        name = request.form.get("name")
        phone = request.form.get("phone")
        username= request.form.get("username")
        password= request.form.get("password")
        parent= Parent.query.get(parent_id)
        parent.name = name
        parent.phone = phone
        parent.username = username
        parent.password = password
        db.session.commit()
        flash(f'Cập nhật thành công thông tin phụ huynh: {name}')
        return redirect(url_for('parent_management'))
    except:
        flash(f'Số điện thoại này đã tồn tại')
        return redirect(url_for('parent_management'))
   


@app.route("/delete_parent/<int:parent_id>")
@login_required
def delete_parent(parent_id):
    parent = Parent.query.get(parent_id)
    name = parent.name
    db.session.delete(parent)
    db.session.commit()
    flash(f'Đã xóa thành công phụ huynh: {name}')
    return redirect(url_for('parent_management'))



# ---------------- Quản lý giáo viên -------------------------------------------------\

@app.route("/teacher_management")
@login_required
def teacher_management():
    teachers = Teacher.query.all()
    return render_template ("teacher_management.html", teachers=teachers)


@app.route("/addNewTeacher_s1")
@login_required
def addNewTeacher_s1():
    class1 = Class.query.all()
    return render_template ("addNewTeacher_s1.html", class1=class1)


@app.route("/addNewTeacher_s2/<int:class_id>")
@login_required
def addNewTeacher_s2(class_id):
    class1 = Class.query.get(class_id)
    return render_template("addNewTeacher_s2.html", class1=class1)


@app.route("/addNewTeacher_s3", methods=["POST"])
@login_required
def addNewTeacher_s3():  
    #Get form information
    try:
        class_id = int(request.form.get("class_id"))
        name = request.form.get("name")
        degree = request.form.get("degree")
        experience = request.form.get("experience")
        address = request.form.get("address")
        phone= request.form.get("phone")
        email= request.form.get("email")
        teacher = Teacher(name=name, degree=degree, experience=experience, address=address, phone=phone, email=email, class_id=class_id)
        db.session.add(teacher)
        db.session.commit()
        flash(f'Đã thêm thành công giáo viên: {name}')
        return redirect(url_for('teacher_management'))
    except:
        flash(f'Số điện thoại hoặc email này đã tồn tại')    
        return redirect(url_for('teacher_management'))


@app.route("/update_teacher/<int:teacher_id>")
@login_required
def update_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return render_template ("update_teacher_s1.html", teacher=teacher)


@app.route("/update_teacher_s1", methods=["POST"])
@login_required
def update_teacher_s1():
    try:
        teacher_id = int(request.form.get("teacher_id"))
        name = request.form.get("name")
        degree = request.form.get("degree")
        experience= request.form.get("experience")
        address= request.form.get("address")
        phone= request.form.get("phone")
        email= request.form.get("email") 
        teacher= Teacher.query.get(teacher_id)
        teacher.name = name
        teacher.degree = degree
        teacher.experience = experience
        teacher.address = address
        teacher.phone = phone
        teacher.email = email
        db.session.commit()
        flash(f'Cập nhật thành công thông tin giáo viên: {name}')
        return redirect(url_for('teacher_management'))
    except:
        flash(f'Số điện thoại hoặc email này đã tồn tại')    
        return redirect(url_for('teacher_management'))



@app.route("/delete_teacher/<int:teacher_id>")
@login_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    name = teacher.name
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Đã xóa thành công giáo viên: {name}')
    return redirect(url_for('teacher_management'))



# -------------------Quản lý hoạt động-------------------------------------------

@app.route("/work_management")
@login_required
def work_management():
    works = Work.query.all()
    class1 = Class.query.all()
    return render_template ("work_management.html", works=works,class1 =class1)


@app.route("/addNewWork_s1")
@login_required
def addNewWork_s1():
    class1 = Class.query.all()
    return render_template ("addNewWork_s1.html", class1=class1)


@app.route("/addNewWork_s2/<int:class_id>")
@login_required
def addNewWork_s2(class_id):
    class1 = Class.query.get(class_id)
    return render_template("addNewWork_s2.html", class1=class1)


@app.route("/addNewWork_s3", methods=["POST"])
@login_required
def addNewWork_s3():  
    #Get form information
    class_id = int(request.form.get("class_id"))
    name = request.form.get("name")
    teacher_name = request.form.get("teacher_name")
    date = request.form.get("date")
    time = request.form.get("time")
    work = Work(name=name, teacher_name=teacher_name, time=time, date=date, class_id=class_id)
    db.session.add(work)
    db.session.commit()
    flash(f'Đã thêm thành công hoạt động:')
    return redirect(url_for('work_management'))


@app.route("/update_work/<int:work_id>")
@login_required
def update_work(work_id):
    work = Work.query.get(work_id)
    return render_template ("update_work_s1.html", work=work)


@app.route("/update_work_s1", methods=["POST"])
@login_required
def update_work_s1():
    work_id = int(request.form.get("work_id"))
    name = request.form.get("name")
    teacher_name = request.form.get("teacher_name")
    date = request.form.get("date")
    time = request.form.get("time")
    work= Work.query.get(work_id)
    work.name = name
    work.teacher_name = teacher_name
    work.date = date
    work.time = time
    db.session.commit()
    flash(f'Cập nhật thành công hoạt động: {name}')
    return redirect(url_for('work_management'))
   


@app.route("/delete_work/<int:work_id>")
@login_required
def delete_work(work_id):
    work = Work.query.get(work_id)
    name = work.name
    db.session.delete(work)
    db.session.commit()
    flash(f'Đã xóa thành công hoạt động: {name}')
    return redirect(url_for('work_management'))



# -----------Quản lý bữa ăn -----------------------------


@app.route("/meal_management")
@login_required
def meal_management():
    meals = Meal.query.all()
    return render_template ("meal_management.html", meals=meals)


@app.route("/addNewMeal_s1")
@login_required
def addNewMeal_s1():
    class1 = Class.query.all()
    return render_template ("addNewMeal_s1.html", class1=class1)


@app.route("/addNewMeal_s2/<int:class_id>")
@login_required
def addNewMeal_s2(class_id):
    class1 = Class.query.get(class_id)
    return render_template("addNewMeal_s2.html", class1=class1)


@app.route("/addNewMeal_s3", methods=["POST"])
@login_required
def addNewMeal_s3():  
    #Get form information
    class_id = int(request.form.get("class_id"))
    name = request.form.get("name")
    time = request.form.get("time")
    meal = Meal(name=name, time=time, class_id=class_id)
    db.session.add(meal)
    db.session.commit()
    flash(f'Đã thêm thành công bữa: {name}')
    return redirect(url_for('meal_management'))


@app.route("/update_meal/<int:meal_id>")
@login_required
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)
    return render_template ("update_meal_s1.html", meal=meal)


@app.route("/update_meal_s1", methods=["POST"])
@login_required
def update_meal_s1():
    meal_id = int(request.form.get("meal_id"))
    name = request.form.get("name")
    time = request.form.get("time")
    meal= Meal.query.get(meal_id)
    meal.name = name
    meal.time = time
    db.session.commit()
    flash(f'Cập nhật thành công bữa: {name}')
    return redirect(url_for('meal_management'))
   


@app.route("/delete_meal/<int:meal_id>")
@login_required
def delete_meal(meal_id):
    try:
        meal = Meal.query.get(meal_id)
        name = meal.name
        time = meal.time
        db.session.delete(meal)
        db.session.commit()
        flash(f'Đã xóa thành công bữa: {name} ngày {time}')
        return redirect(url_for('meal_management'))
    except:
            flash(f'Bạn cần xóa thông tin món ăn liên quan đến bữa ăn này')
            return redirect(url_for('meal_management'))


# --------------Quản lý món ăn-------------------------------------------

@app.route("/dish_management_s1/<int:meal_id>")
@login_required
def dish_management_s1(meal_id):
    dishes = Dish.query.filter(Dish.meal_id == meal_id)
    meal = Meal.query.get(meal_id)
    return render_template ("dish_management.html", dishes=dishes, meal=meal)


@app.route("/addNewDish_s1/<int:meal_id>")
@login_required
def addNewDish_s1(meal_id):
    meal = Meal.query.get(meal_id)
    return render_template ("addNewDish_s1.html", meal=meal)


@app.route("/addNewDish_s2", methods=["POST"])
@login_required
def addNewDish_s2():  
    #Get form information
    meal_id = int(request.form.get("meal_id"))
    name = request.form.get("name")
    dish = Dish(name=name, meal_id=meal_id)
    db.session.add(dish)
    db.session.commit()
    flash(f'Đã thêm thành công món: {name}')
    return redirect(url_for('dish_management_s1', meal_id=meal_id))


@app.route("/update_dish/<int:dish_id>")
@login_required
def update_dish(dish_id):
    dish = Dish.query.get(dish_id)
    return render_template ("update_dish_s1.html", dish=dish)


@app.route("/update_dish_s1", methods=["POST"])
@login_required
def update_dish_s1():
    dish_id = request.form.get("dish_id")
    name = request.form.get("name")
    dish = Dish.query.get(dish_id)
    dish.name = name
    meal_id = dish.meal_id
    db.session.commit()
    flash(f'Cập nhật thành công món: {name}')
    return redirect(url_for('dish_management_s1', meal_id=meal_id))
   


@app.route("/delete_dish/<int:dish_id>")
@login_required
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    meal_id = dish.meal_id
    name = dish.name
    db.session.delete(dish)
    db.session.commit()
    flash(f'Đã xóa thành công món: {name}')
    return redirect(url_for('dish_management_s1', meal_id=meal_id))


# -------------- Quản lý sức khỏe--------------------------------------------

@app.route("/health_management_s1/<int:student_id>")
@login_required
def health_management_s1(student_id):
    # dùng filter thay vì get để lấy nhiều 
    healths = Health.query.filter(Health.student_id == student_id)
    student = Student.query.get(student_id)
    return render_template ("health_management_s1.html", healths=healths, student= student)


@app.route("/health_management")
@login_required
def health_management():
    healths = Health.query.all()
    students = Student.query.all()
    class1 = Class.query.all()
    return render_template ("health_management.html", healths=healths, students=students, class1=class1)


@app.route("/searchStudentForHealth", methods=["GET", "POST"])
@login_required
def searchStudentForHealth():
    id = request.args.get("id")
    students = Student.query.get(id)
    class1 = Class.query.all()
    healths = Health.query.filter(Health.student_id == students.id)
    return render_template ("searchStudentForHealth.html", students=students, class1=class1,  healths=healths)


@app.route("/addNewHealth_s1")
@login_required
def addNewHealth_s1():
    students = Student.query.all()
    return render_template ("addNewHealth_s1.html", students=students)


# Tìm kiếm học sinh để ghi chú tình trạng sức khỏe

@app.route("/searchStudentForAddHealth", methods=["GET","POST"])
@login_required
def searchStudentForAddHealth():
    id = request.args.get("id")
    students = Student.query.get(id)
    return render_template ("selectStudentForAddHealth.html", students=students)
      

# Thêm mới sức khỏe theo id học sinh đang xem
@app.route("/addNewHealth_s2/<int:student_id>")
@login_required
def addNewHealth_s2(student_id):
    student = Student.query.get(student_id)
    return render_template("addNewHealth_s2.html", student=student)


@app.route("/addNewHealth_s3", methods=["POST"])
@login_required
def addNewHealth_s3():  
    #Get form information
    student_id = request.form.get("student_id")
    height = request.form.get("height")
    weight = request.form.get("weight")
    note= request.form.get("note")
    health = Health(height=height, weight=weight, note=note, student_id=student_id)
    db.session.add(health)
    db.session.commit()
    flash(f'Đã thêm thành công')
    return redirect(url_for('health_management'))


# -----Cập nhật thông tin sức khỏe----------------------


@app.route("/update_health/<int:health_id>")
@login_required
def update_health(health_id):
    health = Health.query.get(health_id)
    return render_template ("update_health_s1.html", health=health)


@app.route("/update_health_s1", methods=["POST"])
@login_required
def update_health_s1():
    health_id = request.form.get("health_id")
    height = request.form.get("height")
    weight = request.form.get("weight")
    note= request.form.get("note")
    health= Health.query.get(health_id)
    health.height = height
    health.weight = weight
    health.note = note
    db.session.commit()
    flash(f'Cập nhật thành công thông tin')
    return redirect(url_for('health_management'))
   


@app.route("/delete_health/<int:health_id>")
@login_required
def delete_health(health_id):
    health = Health.query.get(health_id)
    db.session.delete(health)
    db.session.commit()
    flash(f'Đã xóa thành công')
    return redirect(url_for('health_management'))

# -----------------Quản lý học phí-------------------------------------------


@app.route("/tuition_management_s1/<int:student_id>")
@login_required
def tuition_management_s1(student_id):
    # dùng filter thay vì get để lấy nhiều 
    tuitions = Tuition.query.filter(Tuition.student_id == student_id)
    student = Student.query.get(student_id)
    return render_template ("tuition_management_s1.html", tuitions=tuitions, student= student)


@app.route("/tuition_management")
@login_required
def tuition_management():
    tuitions = Tuition.query.all()
    students = Student.query.all()
    class1 = Class.query.all()
    pays = Pay.query.all()
    return render_template ("tuition_management.html", tuitions=tuitions, students=students, class1=class1, pays=pays)


@app.route("/tuition_management_s2/<int:class_id>", methods=["GET", "POST"])
@login_required
def tuition_management_s2(class_id):
    students = Student.query.filter(Student.class_id == class_id)
    class1 = Class.query.all()
    tuitions = Tuition.query.all()
    return render_template ("tuition_management.html", students=students, class1=class1,  tuitions=tuitions)


@app.route("/addNewTuition_s1")
@login_required
def addNewTuition_s1():
    students = Student.query.all()
    return render_template ("addNewTuition_s1.html", students=students)


# Tìm kiếm học sinh để thêm học phí

@app.route("/searchStudentForTuition", methods=["GET","POST"])
@login_required
def searchStudentForTuition():
    id = request.args.get("id")
    student = Student.query.get(id)
    return render_template ("selectStudentForTuition.html", student=student)
     
      
@app.route("/searchStudentForPay", methods=["GET","POST"])
@login_required
def searchStudentForPay():
    id = request.args.get("id")
    students = Student.query.get(id)
    # tuitions = Tuition.query.all()
    tuitions = Tuition.query.filter(Tuition.student_id == students.id)
    class1 = Class.query.filter(Class.id == students.class_id)
    pays = Pay.query.all()
    return render_template ("selectStudentForPay.html", students=students, tuitions=tuitions, class1=class1, pays=pays)



# Thêm mới học phí theo id học sinh đang xem
@app.route("/addNewTuition_s2/<int:student_id>")
@login_required
def addNewTuition_s2(student_id):
    student = Student.query.get(student_id)
    return render_template("addNewTuition_s2.html", student=student)


@app.route("/addNewTuition_s3", methods=["POST"])
@login_required
def addNewTuition_s3():  
    #Get form information
    student_id = int(request.form.get("student_id"))
    tuition_receivable = request.form.get("tuition_receivable")
    tuition_paid= request.form.get("tuition_paid")
    tuition_debt = (int(tuition_receivable) - int(tuition_paid))
    time= request.form.get("time")
    tuition = Tuition(tuition_receivable=tuition_receivable, tuition_paid=tuition_paid, tuition_debt=tuition_debt, time=time, student_id=student_id)
    db.session.add(tuition)
    db.session.commit()
    flash(f'Đã thêm thành công')
    return redirect(url_for('tuition_management'))


# -----Cập nhật thông tin sức khỏe----------------------


@app.route("/update_tuition/<int:tuition_id>")
@login_required
def update_tuition(tuition_id):
    tuition = Tuition.query.get(tuition_id)
    return render_template ("update_tuition_s1.html", tuition=tuition)


@app.route("/update_tuition_s1", methods=["POST"])
@login_required
def update_tuition_s1():
    tuition_id = request.form.get("tuition_id")
    tuition_receivable = request.form.get("tuition_receivable")
    tuition_paid= request.form.get("tuition_paid")
    tuition_debt = request.form.get("tuition_debt")
    time = request.form.get("time")
    tuition= Tuition.query.get(tuition_id)
    tuition.tuition_receivable = tuition_receivable
    tuition.tuition_paid = tuition_paid
    tuition.tuition_debt = tuition_debt
    tuition.time = time
    db.session.commit()
    flash(f'Cập nhật thành công thông tin')
    return redirect(url_for('tuition_management'))
   


@app.route("/delete_tuition/<int:tuition_id>")
@login_required
def delete_tuition(tuition_id):
    try:
        tuition = Tuition.query.get(tuition_id)
        db.session.delete(tuition)
        db.session.commit()
        flash(f'Đã xóa thành công')
        return redirect(url_for('tuition_management'))
    except:
        flash(f'Bạn cần xóa thông tin đóng học liên quan trước khi xóa học phí này')
        return redirect(url_for('tuition_management'))

# ----------------Quản lý thanh toán học phí--------------------------------- 


# @app.route("/tuition_management_s1/<int:student_id>")
# @login_required
# def tuition_management_s1(student_id):
#     # dùng filter thay vì get để lấy nhiều 
#     tuitions = Tuition.query.filter(Tuition.student_id == student_id)
#     student = Student.query.get(student_id)
#     return render_template ("tuition_management_s1.html", tuitions=tuitions, student= student)


@app.route("/pay_management")
@login_required
def pay_management():
    pays = Pay.query.all()
    return render_template ("pay_management.html", pays=pays)


# @app.route("/tuition_management_s2/<int:class_id>", methods=["GET", "POST"])
# @login_required
# def tuition_management_s2(class_id):
#     students = Student.query.filter(Student.class_id == class_id)
#     class1 = Class.query.all()
#     tuitions = Tuition.query.all()
#     return render_template ("tuition_management.html", students=students, class1=class1,  tuitions=tuitions)


# @app.route("/addNewTuition_s1")
# @login_required
# def addNewTuition_s1():
#     students = Student.query.all()
#     return render_template ("addNewTuition_s1.html", students=students)


# # Tìm kiếm học sinh để thêm học phí

# @app.route("/searchStudentForTuition", methods=["GET","POST"])
# @login_required
# def searchStudentForTuition():
#     id = request.args.get("id")
#     students = Student.query.get(id)
#     return render_template ("selectStudentForTuition.html", students=students)
     
      
# @app.route("/searchStudentForPay", methods=["GET","POST"])
# @login_required
# def searchStudentForPay():
#     id = request.args.get("id")
#     students = Student.query.get(id)
#     tuitions = Tuition.query.all()
#     class1 = Class.query.all()
#     return render_template ("selectStudentForPay.html", students=students, tuitions=tuitions, class1=class1)


# Thêm mới học phí theo id học sinh đang xem
@app.route("/addNewPay_s1/<int:tuition_id>")
@login_required
def addNewPay_s1(tuition_id):
    tuition = Tuition.query.get(tuition_id)
    return render_template("addNewPay_s1.html", tuition=tuition)


@app.route("/addNewPay_s2", methods=["POST"])
@login_required
def addNewPay_s2():   
    #Get form information
    tuition_id = int(request.form.get("tuition_id"))
    money = request.form.get("money")
    payer= request.form.get("payer")
    pay = Pay(money=money, payer=payer, tuition_id=tuition_id)
    tuition = Tuition.query.get(tuition_id)
    tuition.tuition_paid = money
    tuition.tuition_debt = (int(tuition.tuition_receivable) - int(tuition.tuition_paid))
    db.session.add(pay)
    db.session.commit()
    flash(f'Đã thêm thành công')
    return redirect(url_for('tuition_management'))


# -----Cập nhật thông tin thanh toán học phí----------------------


@app.route("/update_pay/<int:pay_id>")
@login_required
def update_pay(pay_id):
    pay = Pay.query.get(pay_id)
    return render_template ("update_pay_s1.html", pay=pay)


@app.route("/update_pay_s1", methods=["POST"])
@login_required
def update_pay_s1():
    pay_id = request.form.get("pay_id")
    money= request.form.get("money")
    payer = request.form.get("payer")
    pay= Pay.query.get(pay_id)
    pay.money = money
    pay.payer = payer
    db.session.commit()
    flash(f'Cập nhật thành công thông tin')
    return redirect(url_for('pay_management'))
   


@app.route("/delete_pay/<int:pay_id>")
@login_required
def delete_pay(pay_id):
    pay = Pay.query.get(pay_id)
    db.session.delete(pay)
    db.session.commit()
    flash(f'Đã xóa thành công')
    return redirect(url_for('pay_management'))


# =====================Quản lý tài khoản=========================================


@app.route("/account_management")
@login_required
def account_management():
    users = User.query.all()
    return render_template ("account_management.html", users=users) 


@app.route("/delete_account/<int:user_id>")
@login_required
def delete_account(user_id):
    user = User.query.get(user_id)
    name = user.name
    db.session.delete(user)
    db.session.commit()
    flash(f'Đã xóa thành công tài khoản có tên: {name}')
    return redirect(url_for('account_management'))


 

# -------------- Quản lý thông báo--------------------------------------------

@app.route("/notification_management")
@login_required
def notification_management():
    notifications = Notification.query.all()
    return render_template ("notification_management.html", notifications=notifications)


@app.route("/addNewNotification_s1")
@login_required
def addNewNotification_s1():
    return render_template ("addNewNotification_s1.html")


@app.route("/addNewNotification_s2", methods=["POST"])
@login_required
def addNewNotification_s2():
    name = request.form.get("name")
    content = request.form.get("content")
    notification = Notification(name=name, content=content)
    db.session.add(notification)
    db.session.commit()
    flash(f'Thêm mới thành công thông báo: {name}')
    return redirect(url_for('notification_management'))   





# ----------Upload file----------------------

# UPLOAD_FOLDER = '/static/img'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
# @app.route('/addNewNotification_s2', methods=['GET', 'POST'])
# def addNewNotification_s2():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         name = request.form.get("name")
#         content = request.form.get("content")
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
#         notification = Notification(name=name, content=content, image=name)
#         db.session.add(notification)
#         db.session.commit()
#         flash(f'Thêm mới thành công thông báo: {name}')
#         return redirect(url_for('notification_management', name=filename))
#     return 

# @app.route("/addNewNotification_s2", methods=["POST"])
# @login_required
# def addNewNotification_s2():
#     name = request.form.get("name")
#     content = request.form.get("content")
#     file = request.files['file']

#     # Kiểm tra xem có file được chọn hay không
#     if file.filename == '':
#         flash('Bạn chưa chọn file')
#         return redirect(url_for('notification_management'))

#     # Lưu file vào thư mục cụ thể trên đĩa
#     filename = secure_filename(file.filename)
#     file_path = os.path.join('/static/img', filename)
#     file.save(file_path)

#     # Tạo đối tượng Notification và chèn vào cơ sở dữ liệu
#     notification = Notification(name=name, content=content, image=file_path)
#     db.session.add(notification)
#     db.session.commit()

#     flash(f'Thêm mới thành công thông báo: {name}')
#     return redirect(url_for('notification_management'))


@app.route("/update_notification/<int:notification_id>")
@login_required
def update_notification(notification_id):
    notification = Notification.query.get(notification_id)
    return render_template ("update_notification_s1.html", notification=notification)


@app.route("/update_notification_s2", methods=["POST"])
@login_required
def update_notification_s2():
    notification_id = request.form.get("notification_id")
    name = request.form.get("name")
    content = request.form.get("content")
    notification= Notification.query.get(notification_id)
    notification.name = name
    notification.content = content
    db.session.commit()
    flash(f'Cập nhật thành công thông báo: {name}')
    return redirect(url_for('notification_management'))
   


@app.route("/delete_notification/<int:notification_id>")
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    name = notification.name
    db.session.delete(notification)
    db.session.commit()
    flash(f'Đã xóa thành công thông báo: {name}')
    return redirect(url_for('notification_management'))


#----------------Đăng ký tài khoản------------------------------------------------


@app.route("/signUp_s1", methods=["GET", "POST"])
@login_required
def signUp_s1():
    """show sign up form"""
    
    form = signUpForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        phone = form.phone.data
        NewUser = User(name=name, username=username, password=password, email=email, phone=phone)
        NewUser.set_password(form.password.data)
        # NewPassenger.is_admin = True
        db.session.add(NewUser)
        db.session.commit()
        flash('Tạo tài khoản thành công!')
        return redirect(url_for('index'))
    return render_template("signUp_s1.html", form=form)


# ---------------Đăng nhập admin-------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # nếu không có người dùng or mật khẩu k trùng 
        if user is None or not user.check_password(form.password.data):
            flash('Tên tài khoản hoặc mật khẩu không chính xác.')
            return redirect(url_for('login'))
        # Tải dữ liệu liên quan đến người dùng
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') #Tham số next đc gán giá trị của url yêu cầu ban đầu
        if not next_page:                      #từ đó ứng dụng sẽ biết cần phải trở lại trang tr khi admin đăng nhập thành công
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Đăng nhập', form=form)

    

# # ---------------Đăng nhập parent-------------------------------------------------

@app.route('/login_parent', methods=['GET', 'POST'])
def login_parent():
    if current_user.is_authenticated:
        return redirect(url_for('index_parent'))
    form = ParentLoginForm()
    if form.validate_on_submit():
        parent = Parent.query.filter_by(username=form.username.data).first()
        # nếu không có người dùng or mật khẩu k trùng 
        if parent is None or not parent.check_password(form.password.data):
        # if parent is not None and parent.check_password(form.password.data): 
            flash('Tên tài khoản hoặc mật khẩu không chính xác.')
            return redirect(url_for('login_parent'))
        # Tải dữ liệu liên quan đến người dùng
        login_user(parent, remember=form.remember_me.data)
        next_page = request.args.get('next') #Tham số next đc gán giá trị của url yêu cầu ban đầu
        if not next_page:                      #từ đó ứng dụng sẽ biết cần phải trở lại trang tr khi admin đăng nhập thành công
            next_page = url_for('index_parent')
        return redirect(next_page)
    return render_template('login_parent.html', title='Đăng nhập', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# @app.route('/login_parent', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         if request.path == '/login':
#             return redirect(url_for('index'))
#         else:
#             return redirect(url_for('index_parent'))
    
#     form = loginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         parent = Parent.query.filter_by(username=form.username.data).first()
        
#         if request.path == '/login':
#             if user is None or not user.check_password(form.password.data):
#                 flash('Tên tài khoản hoặc mật khẩu không chính xác.')
#                 return redirect(url_for('login'))
#             login_user(user, remember=form.remember_me.data)
#             next_page = request.args.get('next')
#             if not next_page:
#                 next_page = url_for('index')
#             return redirect(next_page)
        
#         elif request.path == '/login_parent':
#             if parent is None or not parent.check_password(form.password.data):
#                 flash('Tên tài khoản hoặc mật khẩu không chính xác.')
#                 return redirect(url_for('login'))
#             login_user(parent, remember=form.remember_me.data)
#             next_page = request.args.get('next')
#             if not next_page:
#                 next_page = url_for('index')
#             return redirect(next_page)
    
#     return render_template('login.html', title='Đăng nhập', form=form)

# ------------------Đăng nhập admin vs phụ huynh----------------------------------------------

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index_parent'))

#     form = loginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         parent = Parent.query.filter_by(username=form.username.data).first()

#         if user is not None and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             next_page = request.args.get('next')
#             if not next_page:
#                 return redirect(url_for('index'))
#             return redirect(next_page)

#         elif parent is not None and parent.check_password(form.password.data): 
#             login_user(parent, remember=form.remember_me.data)
#             # next_page = request.args.get('next')
#             # if not next_page:
#             #     return render_template('index_parent.html', parent=parent)
#             #     # return redirect(url_for('index_parent'))
#             # return redirect(next_page)
#             return render_template('index_parent.html', parent=parent)

#         else:
#             flash('Tên tài khoản hoặc mật khẩu không chính xác.')
#             return redirect(url_for('login'))

#     return render_template('login.html', title='Đăng nhập', form=form)

# ------------------Đăng xuất------------------------------

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# ----------------------------------------

@app.route('/logout_parent')
def logout_parent():
    logout_user()
    return redirect(url_for('login_parent'))

# =============================================================================================

# ------------------Giao diện parent----------------

@app.route('/index_parent')
def index_parent():
    parents = Parent.query.all()
    return render_template('index_parent.html', parents=parents)


# ------------------Thông tin học sinh-------------------------------

@app.route('/info_student/<int:parent_id>')
def info_student(parent_id):
    parent = Parent.query.get(parent_id)
    student = Student.query.get(parent.student_id)
    class1 = Class.query.all()
    return render_template("info_student.html", student=student, parent=parent, class1 = class1)


@app.route('/info_teacher/<int:class_id>')
def info_teacher(class_id):
    teachers = Teacher.query.filter(Teacher.class_id == class_id)
    return render_template("info_teacher.html", teachers=teachers)


@app.route('/info_health/<int:parent_id>')
def info_health(parent_id):
    parent = Parent.query.get(parent_id)
    student = Student.query.get(parent.student_id)
    healths = Health.query.filter(Health.student_id == student.id)
    return render_template("info_health.html", healths=healths, student=student)


@app.route('/info_tuition/<int:parent_id>')
def info_tuition(parent_id):
    parent = Parent.query.get(parent_id)
    student = Student.query.get(parent.student_id)
    tuitions = Tuition.query.filter(Tuition.student_id == student.id)
    class1 = Class.query.all()
    pays = Pay.query.all()
    return render_template("info_tuition.html", tuitions=tuitions, student=student, class1=class1, pays=pays)


@app.route('/info_work/<int:parent_id>')
def info_work(parent_id):
    parent = Parent.query.get(parent_id)
    student = Student.query.get(parent.student_id)
    class1 = Class.query.get(student.class_id)
    works = Work.query.filter(Work.class_id == class1.id)
    return render_template("info_work.html", works=works)


@app.route('/info_meal/<int:parent_id>')
def info_meal(parent_id):
    parent = Parent.query.get(parent_id)
    student = Student.query.get(parent.student_id)
    class1 = Class.query.get(student.class_id)
    meals = Meal.query.filter(Meal.class_id == class1.id)
    dishs = Dish.query.all()
    return render_template("info_meal.html", meals=meals, dishs=dishs)


@app.route('/info_notification/')
def info_notification():
    notifications = Notification.query.all()
    return render_template("info_notification.html", notifications=notifications )


@app.route('/content_notification/<int:notification_id>')
def content_notification(notification_id):
    notification = Notification.query.get(notification_id)
    return render_template("content_notification.html", notification=notification)
