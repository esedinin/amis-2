from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField, SelectField
from wtforms import validators
from source.dao.orm.entities import Group
from connection import db

def get_student_groups():
    ch = []
    groups = sorted(list(db.sqlalchemy_session.query(Group.group_name).distinct()))
    pers = []
    for i in range(len(groups)):
        pers.append(groups[i][0])
    for i in range(len(groups)):
        tuple = groups[i][0], groups[i][0]
        ch.append(tuple)
    return ch

class StudentForm(Form):
    @staticmethod
    def reload_groups():
        StudentForm.student_group = SelectField("Group: ", [
        validators.DataRequired("Please enter student Group."),
        ],
                                choices=get_student_groups(), coerce=str)


    student_id = HiddenField()

    group_id = HiddenField()

    student_name = StringField("name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    student_group = SelectField("Group: ", [
        validators.DataRequired("Please enter student Group."),
        ],
                                choices=get_student_groups(), coerce=str)

    student_university = StringField("university: ", [
        validators.DataRequired("Please enter student university.")])

    student_faculty = StringField("faculty: ", [
        validators.DataRequired("Please enter student faculty.")])

    house_id = IntegerField("house_id: ")

    submit = SubmitField("Save")
