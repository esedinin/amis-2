from flask_wtf import Form
from wtforms import SubmitField, BooleanField, HiddenField, SelectField, DateField, StringField
from wtforms import validators
from source.dao.db import *
from source.dao.orm.entities import *
from connection import db

def get_attendance_students():
    ch = []
    students = sorted(list(db.sqlalchemy_session.query(Student.student_name).distinct()))
    pers = []
    for i in range(len(students)):
        pers.append(students[i][0])
    for i in range(len(students)):
        tuple = students[i][0], students[i][0]
        ch.append(tuple)
    return ch

def get_attendance_disciplines():
    ch = []
    disciplines = sorted(list(db.sqlalchemy_session.query(Discipline.discipline_name).distinct()))
    pers = []
    for i in range(len(disciplines)):
        pers.append(disciplines[i][0])
    for i in range(len(disciplines)):
        tuple = disciplines[i][0], disciplines[i][0]
        ch.append(tuple)
    return ch

# def get_attendance_dates():
#     ch = []
#     dates = sorted(list(db.sqlalchemy_session.query(Schedule.class_date).distinct()))
#     pers = []
#     for i in range(len(dates)):
#         pers.append(dates[i][0])
#     for i in range(len(dates)):
#         tuple = dates[i][0], dates[i][0]
#         ch.append(tuple)
#     return ch

class AttendanceForm(Form):
    @staticmethod
    def reload_students():
        AttendanceForm.student_name = SelectField("Student: ", [
            validators.DataRequired("Please enter student."),
        ], choices=get_attendance_students(), coerce=str)

    @staticmethod
    def reload_disciplines():
        AttendanceForm.discipline_name = SelectField("Discipline: ", [
            validators.DataRequired("Please enter discipline."),
        ], choices=get_attendance_disciplines(), coerce=str)

    # @staticmethod
    # def reload_dates():
    #     AttendanceForm.class_date = DateField("Date: ", [validators.DataRequired("Please enter discipline name.")], format='%Y-%m-%d')

    attendance_id = HiddenField()
    student_id = HiddenField()

    student_name = SelectField("Student: ", [
        validators.DataRequired("Please enter student."),
    ], choices=get_attendance_students(), coerce=str)

    class_id = HiddenField()

    discipline_name = SelectField("discipline name: ", [
        validators.DataRequired("Please enter discipline name."),
    ], choices=get_attendance_disciplines(), coerce=str)

    class_date = DateField("Date: ", [validators.DataRequired("Please enter discipline name.")], format='%Y-%m-%d')

    attended = BooleanField("attended: ")

    submit = SubmitField("Save")
