from flask_wtf import Form
from wtforms import SubmitField, IntegerField, BooleanField, HiddenField
from wtforms import validators


class AttendanceForm(Form):
    attendance_id = HiddenField()

    student_id = IntegerField("student id: ", [
        validators.DataRequired("Please enter student id.")
    ])

    class_id = IntegerField("class_id: ", [
        validators.DataRequired("Please enter class id.")
    ])

    attended = BooleanField("attended: ")

    submit = SubmitField("Save")
