import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Student
from App.models import Staff
from App.models import Shortlist
from App.models import Intern
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    jeff = User(username='jeff', password ='jeffpass')
    tito = User(username='tito',password='titopass')
    oold =  User(username='oold', password ='ooldpass')

    mic = Student(username = 'mic',password='micpass')
    klim = Student(username = 'klim',password='klimpass')
    hioo = Student(username = 'hioo',password='hioopass')

    dairy = Staff(username='dairy',password='dairypass')
    potato = Staff(username='potato',password='potatopass')
    tom = Staff(username='tom',password='tompass')

    db.session.add_all([jeff,tito,oold,mic,klim,hioo,dairy,tom,potato])
    db.session.commit()
    emp = User.query.all()
    stu = Student.query.all()
    staff =  Staff.query.all()
    print('database intialized')
    print('this is emp ' +str(emp))
    print("this is students " + str(stu))
    print("this is staff " + str(staff))


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@app.cli.command("create_user", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass
@app.cli.command("create_student", help="Creates a student")
@click.argument("username", default="jim")
@click.argument("password", default="jimpass")
def create_student_command(username, password):
    stu =  Student(username=username, password=password)
    db.session.add(stu)
    db.session.commit()
    print(f'{username} created!')

@app.cli.command("create_staff", help="Creates a staff")
@click.argument("username", default="tim")
@click.argument("password", default="timpass")
def create_student_command(username, password):
    staff =  Staff(username=username, password=password)
    db.session.add(staff)
    db.session.commit()
    print(f'{username} created!')

@app.cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        emp = User.query.all()
        stu = Student.query.all()
        staff =  Staff.query.all()
        list = Shortlist.query.all()
        inter = Intern.query.all()
        print('this is emp ' +str(emp))
        print("this is students " + str(stu))
        print("this is staff " + str(staff))
        print("this is SHORTLIST " + str(list))
        print("this is inter" + str(inter))

app.cli.add_command(user_cli) # add the group to the cli

@app.cli.command("create_intern", help="Creates an intern application")
def create_intern():
    from App.models import Shortlist
    emp = User.query.all()
    print('list of emp ' +str(emp))
    employer = input('Please enter emp id :')
    emp = User.query.get(employer)
    print(str(emp))
    title = input('Please enter intern title:')
    description = input('Please enter intern description:')
    oo= emp.create_intern(title,description)
    print(str(oo))
   
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@app.cli.command("add_student", help=" Add student to an internship shortlist")
def add_student():
    staff = Staff.query.all()
    print('list of staff ' +str(staff))
    staff_id = input('please enter a staff id:')
    stafff = Staff.query.get(staff_id)
    print(str(stafff))
    list= Intern.query.all()
    print('list of intern '+ str(list))
    int_id= input('please enter an intern id:')
    inter= Intern.query.filter_by(id=int_id).first()
    print(str(inter.id))
    skl = Student.query.all()
    print('list of students '+ str(skl))
    student_id =  input('please enter a student id:')
    stu = Student.query.get(student_id)
    p = stafff.add_intern(intern_id=inter.id,student_id=stu.id)
    print(str(p))

@app.cli.command("evaluate_shortlist", help=" accept/reject student from shortlist")
def evaluate_shortlist():
    emp = User.query.all()
    print(('list of emp ' + str(emp)))
    employer = input('please entera employer id: ')
    emp1 = User.query.get(employer)
    ll = Intern.query.filter_by(user_id=emp1.id).first()
    print('list of inter: '+ str(ll))
    inter_is=input('please enter a intern id:')
    shortlist = Shortlist.query.filter_by(intern_id=inter_is).all()
    print('list of shortlist '+ str(shortlist))
    list_id = input('please enter a shortlist id: ')
    sl = Shortlist.query.get(list_id)
    response = input('accept or reject: ')
    if response == 'accept' or response == 'reject':
        emp1.review_app(response,sl)
        print(str(sl))

@app.cli.command("view_reply", help=" view shortlisted positions and employer response")
def view_reply():
    student = Student.query.all()
    print('list of students  ' + str(student))
    student_id = input('please enter student id:')
    stu = Student.query.get(student_id)
    list = Shortlist.query.filter_by(student_id=stu.id).all()
    print('list of shortlist :' + str(list))
    
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)