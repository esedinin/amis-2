from flask import Flask, render_template, request, redirect, url_for
from source.dao.orm.entities import *
from source.dao.db import PostgresDb
from datetime import date
from source.dao.data import *
from sqlalchemy import func
from source.forms.student_form import StudentForm
from source.forms.group_form import GroupForm
from source.forms.discipline_form import DisciplineForm
from source.forms.house_form import HouseForm
from source.forms.search_student_form import StudentSearchForm
import json
import plotly
import plotly.graph_objs as go
import os

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{host}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    pie_labels = []
    data = {}

    # pie plot -------------------------------------------------------------------------------------------------------
    student_form = StudentSearchForm()
    student_form.init()

    for query, label in zip(*student_form.search(method=request.method)):

        if not query:
            continue

        groups, counts = zip(*query)
        pie = go.Pie(
            labels=[f'group = {group}' for group in groups],
            values=counts
        )
        data[label] = [pie]
        pie_labels.append(label)
    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', json=json_data, pie_labels=pie_labels, student_form=student_form)

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/student', methods=['GET'])
def index_student():
    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Student).all()
    else:
        result = db.sqlalchemy_session.query(Student).all()
        deleted = False

    return render_template('student.html', students=result, deleted=deleted)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()
    db = PostgresDb()

    if request.method == 'POST':
        if not form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Student.student_id)))[0][0]
            student_obj = Student(
                student_id = id  + 1,
                student_university=form.student_university.data,
                student_faculty=form.student_faculty.data,
                student_group=form.student_group.data,
                student_name=form.student_name.data)

            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = StudentForm()

    if request.method == 'GET':

        student_id = request.args.get('student_id')
        db = PostgresDb()
        student = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()

        # fill form and send to student
        form.student_id.data = student.student_id
        form.student_name.data = student.student_name
        form.student_group.data = student.student_group
        form.student_university.data = student.student_university
        form.student_faculty.data = student.student_faculty

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")

    else:

        if not form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            db = PostgresDb()
            # find student
            student = db.sqlalchemy_session.query(Student).filter(Student.student_id == form.student_id.data).one()

            # update fields from form data
            student.student_id = form.student_id.data
            student.student_university = form.student_university.data
            student.student_faculty = form.student_faculty.data
            student.student_group = form.student_group.data
            student.student_name = form.student_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))


@app.route('/delete_student')
def delete_student():
    student_id = request.args.get('student_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()
    result.student_date_expelled = date.today()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_student'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# GROUP ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/group', methods=['GET'])
def index_group():
    db = PostgresDb()

    group = db.sqlalchemy_session.query(Group).all()

    return render_template('group.html', groups=group)


@app.route('/new_group', methods=['GET', 'POST'])
def new_group():
    form = GroupForm()
    db = PostgresDb()
    if request.method == 'POST':
        if not form.validate():
            return render_template('group_form.html', form=form, form_name="New group",
                                   action="new_group")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Group.group_id)))[0][0]
            group_obj = Group(
                group_id = id + 1,
                group_name=form.group_name.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(group_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_group'))

    return render_template('group_form.html', form=form, form_name="New group", action="new_group")


@app.route('/edit_group', methods=['GET', 'POST'])
def edit_group():
    form = GroupForm()

    if request.method == 'GET':

        group_id = request.args.get('group_id')
        db = PostgresDb()
        group = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()

        # fill form and send to group
        form.group_id.data = group.group_id
        form.group_name.data = group.group_name

        return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")

    else:

        if not form.validate():
            return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")
        else:
            db = PostgresDb()
            # find group
            group = db.sqlalchemy_session.query(Group).filter(Group.group_id == form.group_id.data).one()

            # update fields from form data
            group.group_id = form.group_id.data
            group.group_name = form.group_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_group'))


@app.route('/delete_group')
def delete_group():
    group_id = request.args.get('group_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()
    result.group_date_expelled = date.today()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_group'))



# END group ORIENTED QUERIES -----------------------------------------------------------------------------------

# discipline ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/discipline', methods=['GET'])
def index_discipline():
    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Discipline).all()
    else:
        result = db.sqlalchemy_session.query(Discipline).all()
        deleted = False

    return render_template('discipline.html', disciplines=result, deleted=deleted)


@app.route('/new_discipline', methods=['GET', 'POST'])
def new_discipline():
    form = DisciplineForm()
    db = PostgresDb()

    if request.method == 'POST':
        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Discipline.discipline_id)))[0][0]
            discipline_obj = Discipline(
                discipline_id = id + 1,
                discipline_group=form.discipline_group.data,
                discipline_name=form.discipline_name.data)

            db.sqlalchemy_session.add(discipline_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")


@app.route('/discipline', methods=['GET', 'POST'])
def edit_discipline():
    form = DisciplineForm()

    if request.method == 'GET':

        discipline_id = request.args.get('discipline_id')
        db = PostgresDb()
        discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).one()

        # fill form and send to discipline
        form.discipline_id.data = discipline.discipline_id
        form.discipline_name.data = discipline.discipline_name
        form.discipline_group.data = discipline.discipline_group

        return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")

    else:

        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")
        else:
            db = PostgresDb()
            # find discipline
            discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == form.discipline_id.data).one()

            # update fields from form data
            discipline.discipline_id = form.discipline_id.data
            discipline.discipline_group = form.discipline_group.data
            discipline.discipline_name = form.discipline_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))


@app.route('/delete_discipline')
def delete_discipline():
    discipline_id = request.args.get('discipline_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).one()
    result.discipline_date_expelled = date.today()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_discipline'))


# END discipline ORIENTED QUERIES ----------------------------------------------------------------------------------------

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/house', methods=['GET'])
def index_house():
    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(House).all()
    else:
        result = db.sqlalchemy_session.query(House).all()
        deleted = False

    return render_template('house.html', houses=result, deleted=deleted)


@app.route('/new_house', methods=['GET', 'POST'])
def new_house():
    form = HouseForm()
    db = PostgresDb()

    if request.method == 'POST':
        if not form.validate():
            return render_template('house_form.html', form=form, form_name="New house", action="new_house")
        else:
            id = list(db.sqlalchemy_session.query(func.max(House.house_id)))[0][0]
            house_obj = House(
                house_id = id  + 1,
                address=form.address.data,
                price=form.price.data,
                floor_count=form.floor_count.data,
                year=form.year.data)

            db.sqlalchemy_session.add(house_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_house'))

    return render_template('house_form.html', form=form, form_name="New house", action="new_house")


@app.route('/edit_house', methods=['GET', 'POST'])
def edit_house():
    form = HouseForm()

    if request.method == 'GET':

        house_id = request.args.get('house_id')
        db = PostgresDb()
        house = db.sqlalchemy_session.query(House).filter(House.house_id == house_id).one()

        # fill form and send to house
        form.house_id.data = house.house_id
        form.address.data = house.address
        form.price.data = house.price
        form.floor_count.data = house.floor_count
        form.year.data = house.year

        return render_template('house_form.html', form=form, form_name="Edit house", action="edit_house")

    else:

        if not form.validate():
            return render_template('house_form.html', form=form, form_name="Edit house", action="edit_house")
        else:
            db = PostgresDb()
            # find house
            house = db.sqlalchemy_session.query(House).filter(House.house_id == form.house_id.data).one()

            # update fields from form data
            house.house_id = form.house_id.data
            house.address = form.address.data
            house.price = form.price.data
            house.floor_count = form.floor_count.data
            house.year = form.year.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_house'))


@app.route('/delete_house')
def delete_house():
    house_id = request.args.get('house_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(House).filter(House.house_id == house_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_house'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
