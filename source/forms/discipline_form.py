from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, SelectField
from wtforms import validators
from datetime import date


from source.dao.db import PostgresDb
from source.dao.orm.entities import Group

db = PostgresDb()

ch = []
groups = sorted(list(db.sqlalchemy_session.query(Group.group_name).distinct()))
pers = []
for i in range(len(groups)):
    pers.append(groups[i][0])
for i in range(len(groups)):
    tuple = groups[i][0], groups[i][0]
    ch.append(tuple)
print("TUPLE SHOULD BE RENEWED")


class DisciplineForm(Form):
    discipline_id = HiddenField()

    discipline_name = StringField("name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    discipline_group = SelectField("Group: ", [
        validators.DataRequired("Please enter student Group."),
    ],
                                   choices=ch, coerce=str)

    submit = SubmitField("Save")
