from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField, BooleanField
from wtforms import validators


class GroupForm(Form):
    group_id = HiddenField()
    group_name = StringField("name: ", [
        validators.DataRequired("Please enter group name."),])

    submit = SubmitField("Save")
