from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, SelectField
from wtforms import validators
from datetime import date


from source.dao.db import PostgresDb
from source.dao.orm.entities import Group

db = PostgresDb()

def get_discipline_groups():
    ch = []
    groups = sorted(list(db.sqlalchemy_session.query(Group.group_name).distinct()))
    pers = []
    for i in range(len(groups)):
        pers.append(groups[i][0])
    for i in range(len(groups)):
        tuple = groups[i][0], groups[i][0]
        ch.append(tuple)
    return ch


class DisciplineForm(Form):
    @staticmethod
    def reload_groups():
        DisciplineForm.student_group = SelectField("Group: ", [
            validators.DataRequired("Please enter discipline Group."),
        ],
                                                choices=get_discipline_groups(), coerce=str)
    discipline_id = HiddenField()

    discipline_name = StringField("name: ", [
        validators.DataRequired("Please enter discipline name."),
    ])

    discipline_group = SelectField("Group: ", [
        validators.DataRequired("Please enter discipline Group."),
    ],
                                   choices=get_discipline_groups(), coerce=str)

    submit = SubmitField("Save")
