from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField
from wtforms import validators

from source.dao import db
from source.dao.db import PostgresDb
from source.dao.orm.entities import Student

db = PostgresDb()


def get_search_students():
    ch = []
    students = sorted(list(db.sqlalchemy_session.query(Student.student_name).distinct()))
    pers = []
    for i in range(len(students)):
        pers.append(students[i][0])
    for i in range(len(students)):
        tuple = students[i][0], students[i][0]
        ch.append(tuple)
    return ch


class StudentSearchForm(FlaskForm):
    @staticmethod
    def reload_students():
        StudentSearchForm.student = SelectField("Choose student for search: ", [
            validators.DataRequired("Please enter student."),
        ],
                                                choices=get_search_students(), coerce=str)
    id = HiddenField()

    # faculty = StringField("Введіть факультет для виявлення психотипу студентів: ", [
    #     validators.data_required("Це поле є обов'язковим"),
    #     validators.any_of(grps)])

    student = SelectField("Choose student for search: ", [
        validators.DataRequired("Please enter student")], choices=get_search_students())

    submit = SubmitField("Search")