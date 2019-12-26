from flask_wtf import Form
from wtforms import SelectField, SubmitField, BooleanField
from sqlalchemy import func
from source.dao.orm.entities import *
from connection import db

class StudentSearchForm(Form):
    name = SelectField("name:", choices=[("", "---")])
    group = SelectField("group:", choices=[("", "---")])
    university = SelectField("university:", choices=[("", "---")])
    faculty = SelectField("faculty:", choices=[("", "---")])
    submit = SubmitField("Search")

    def init(self):

        self.name.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_name).distinct(Student.student_name).all())]

        self.group.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_group).distinct(Student.student_group).all())]

        self.university.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_university).distinct(Student.student_university).all())]

        self.faculty.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_faculty).distinct(Student.student_faculty).all())]

    def search(self, method):
        result, labels = [], []

        query = db.sqlalchemy_session.query(Student.student_university, Student.student_faculty).distinct(
            Student.student_university, Student.student_faculty)

        if method == 'POST':
            if self.university.data and self.university.data != "None":
                query = query.filter(Student.student_university == self.university.data)
            if self.faculty.data and self.faculty.data != "None":
                query = query.filter(Student.student_faculty == self.faculty.data)

        student_uni_and_faculty_set = query.all()

        for uni, faculty in student_uni_and_faculty_set:

            query = db.sqlalchemy_session.query(Student.student_group, func.count(Student.student_name)).group_by(
                Student.student_group).filter(Student.student_university == uni, Student.student_faculty == faculty)

            if method == "POST":
                if self.group.data and self.group.data != "None":
                    query = query.filter(Student.student_group == self.group.data)
                if self.name.data and self.name.data != "None":
                    query = query.filter(Student.student_name == self.name.data)
            result.append(query.all())
            labels.append(f'university {uni}, faculty {faculty}')
        return result, labels
