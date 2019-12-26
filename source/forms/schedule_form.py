from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, SelectField
from wtforms import validators

from source.dao.db import PostgresDb
from source.dao.orm.entities import Discipline

db = PostgresDb()



def get_schedule_disciplines():
    ch = []
    disciplines = sorted(list(db.sqlalchemy_session.query(Discipline.discipline_name).distinct()))
    pers = []
    for i in range(len(disciplines)):
        pers.append(disciplines[i][0])
    for i in range(len(disciplines)):
        tuple = disciplines[i][0], disciplines[i][0]
        ch.append(tuple)
    return ch


class ScheduleForm(Form):
    @staticmethod
    def reload_disciplines():
        ScheduleForm.discipline_name = SelectField("Discipline: ", [
            validators.DataRequired("Please enter discipline name."),
        ],
                                                   choices=get_schedule_disciplines(), coerce=str)

    class_id = HiddenField()

    # discipline_id = IntegerField("discipline_id: ", [
    #     validators.DataRequired("Please enter discipline id.")
    # ])

    discipline_name = SelectField("Discipline: ", [
        validators.DataRequired("Please enter discipline name."),
        ],
                                choices=get_schedule_disciplines(), coerce=str)

    lecture_hall = StringField("Lecture hall: ")

    class_date = DateField("Class date: ", [validators.DataRequired("Please enter class date.")],
                           format='%Y-%m-%d')

    submit = SubmitField("Save")
