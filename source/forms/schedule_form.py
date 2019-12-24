from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField
from wtforms import validators


class ScheduleForm(Form):
    class_id = HiddenField()

    discipline_id = IntegerField("discipline_id: ", [
        validators.DataRequired("Please enter discipline id.")
    ])

    lecture_hall = StringField("Lecture hall: ")

    class_date = DateField("Class date: ", [validators.DataRequired("Please enter class date.")],
                           format='%Y-%m-%d')

    submit = SubmitField("Save")
