from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField, SelectField
from wtforms import validators
from source.dao.db import PostgresDb
from source.dao.orm.entities import Group
db = PostgresDb()


def update_groups_list():
    ch = []
    groups = sorted(list(db.sqlalchemy_session.query(Group.group_name).distinct()))
    pers = []
    for i in range(len(groups)):
        pers.append(groups[i][0])
    for i in range(len(groups)):
        tuple = groups[i][0], groups[i][0]
        ch.append(tuple)
    print("TUPLE SHOULD BE RENEWED")
    return ch



ch = update_groups_list()


class StudentForm(Form):
    student_id = HiddenField()

    group_id = HiddenField()

    student_name = StringField("name: ", [
        validators.DataRequired("Please enter student name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    student_group = SelectField("Group: ", [
        validators.DataRequired("Please enter student Group."),
        ],
                                choices=ch, coerce=str)

    student_university = StringField("university: ", [
        validators.DataRequired("Please enter student university."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    student_faculty = StringField("faculty: ", [
        validators.DataRequired("Please enter student faculty."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    house_id = IntegerField("house_id: ")

    submit = SubmitField("Save")
