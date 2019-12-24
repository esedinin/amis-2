from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField
from wtforms import validators
from datetime import date


class StudentForm(Form):
    student_id = HiddenField()

    group_id = HiddenField()

    student_name = StringField("name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    student_group = StringField("Group: ", [
        validators.DataRequired("Please enter student Group."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    student_university = StringField("university: ", [
        validators.DataRequired("Please enter student university."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    student_faculty = StringField("faculty: ", [
        validators.DataRequired("Please enter student faculty."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    house_id = IntegerField("house_id: ")

    submit = SubmitField("Save")
