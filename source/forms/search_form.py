from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField
from wtforms import validators

from source.dao import db
from source.dao.db import PostgresDb
from source.dao.orm.entities import Group

db = PostgresDb()


def get_search_groups():
    ch = []
    groups = sorted(list(db.sqlalchemy_session.query(Group.group_name).distinct()))
    pers = []
    for i in range(len(groups)):
        pers.append(groups[i][0])
    for i in range(len(groups)):
        tuple = groups[i][0], groups[i][0]
        ch.append(tuple)
    return ch


class SearchForm(FlaskForm):
    @staticmethod
    def reload_groups():
        SearchForm.group = SelectField("Group: ", [
            validators.DataRequired("Please enter student Group."),
        ],
                                                choices=get_search_groups(), coerce=str)
    id = HiddenField()

    # faculty = StringField("Введіть факультет для виявлення психотипу студентів: ", [
    #     validators.data_required("Це поле є обов'язковим"),
    #     validators.any_of(grps)])

    group = SelectField("Choose group for search: ", [
        validators.DataRequired("Please enter group")], choices=get_search_groups())

    submit = SubmitField("Search")