from flask import Flask, render_template, request, redirect, url_for
# from source.dao.orm.populate import *
from datetime import date
from source.dao.data import *
from source.dao.orm.entities import *
from sqlalchemy import func, and_


import plotly
import plotly.graph_objects as go

from source.forms.student_form import *
from source.forms.group_form import GroupForm
from source.forms.discipline_form import *
from source.forms.house_form import HouseForm
from source.forms.student_attendance_form import StudentSearchForm
from source.forms.schedule_form import ScheduleForm
from source.forms.attendance_form import AttendanceForm
from source.forms.search_form import SearchForm
from source.dao.db import *
import json
import plotly
import plotly.graph_objs as go
import os
from connection import db
from data_analysis import predict

# Base.metadata.create_all(db.sqlalchemy_engine)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{host}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

@app.route('/correlation', methods = ['GET', 'POST'])
def attendance_discipline_correlation():
    result = predict()
    return render_template("correlation.html", result=result)

@app.route('/try', methods=['POST', 'GET'])
def group_attendance():
    form = SearchForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("search_by_group.html", form=form, action="try", form_name="Search students")
        else:
            group_parameter = form.group.data
            print(group_parameter)

            result = db.sqlalchemy_session.query(Discipline.discipline_name, func.count(Student.student_id).filter(Attendance.attended))\
                .join(Schedule, Discipline.discipline_id == Schedule.discipline_id).\
                join(Attendance, Schedule.class_id == Attendance.class_id).\
                join(Student, Student.student_id == Attendance.student_id).group_by(Discipline.discipline_name)\
                .filter(Student.student_group == group_parameter)

            for row in result:
                print(row)
            disciplines = dict((group, count) for group, count in result)
            print(disciplines)
            disciplines_invert = dict((count, group) for group, count in result)
            print(disciplines_invert)
            maxkey = disciplines_invert[max(disciplines.values())]
            print(max(disciplines.values()), 'and its key ', maxkey)

            x = []
            y = []
            for a in disciplines.keys():
                x.append(a)
            for b in disciplines.values():
                y.append(b)
            x.append('Total classes per student')
            print(x)
            for row in db.sqlalchemy_session.query(func.count(Student.student_id))\
                .join(Attendance, Student.student_id == Attendance.student_id).filter(Student.student_group == group_parameter):

                y.append(row[0])
            print(y)
            data = [
                go.Bar(
                    x=x,  # assign x as the dataframe column 'x'
                    y=y
                )
            ]

            graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

            bar = graphJSON
            return render_template('graphics_group.html', plot=bar, group=group_parameter)

    return render_template("search_by_group.html", form=form, action="try", form_name="Serach disciplines in groups")

@app.route('/try2', methods=['POST', 'GET'])
def student_attendance():
    form = StudentSearchForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("search_by_student.html", form=form, action="try2", form_name="Search students")
        else:
            student_parameter = form.student.data
            print(student_parameter)

            result = db.sqlalchemy_session.query(Discipline.discipline_name, func.count(Student.student_id).filter(Attendance.attended))\
                .join(Schedule, Discipline.discipline_id == Schedule.discipline_id).\
                join(Attendance, Schedule.class_id == Attendance.class_id).\
                join(Student, Student.student_id == Attendance.student_id).group_by(Discipline.discipline_name)\
                .filter(Student.student_name == student_parameter)

            for row in result:
                print(row)
            disciplines = dict((student, count) for student, count in result)
            print(disciplines)
            disciplines_invert = dict((count, student) for student, count in result)
            print(disciplines_invert)
            maxkey = disciplines_invert[max(disciplines.values())]
            print(max(disciplines.values()), 'and its key ', maxkey)

            x = []
            y = []
            for a in disciplines.keys():
                x.append(a)
            for b in disciplines.values():
                y.append(b)
            x.append('Total classes per student')
            print(x)
            for row in db.sqlalchemy_session.query(func.count(Student.student_id))\
                .join(Attendance, Student.student_id == Attendance.student_id).filter(Student.student_name == student_parameter):

                y.append(row[0])
            print(y)
            data = [
                go.Bar(
                    x=x,  # assign x as the dataframe column 'x'
                    y=y
                )
            ]

            graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

            bar = graphJSON
            return render_template('graphics_student.html', plot=bar, student=student_parameter)

    return render_template("search_by_student.html", form=form, action="try2", form_name="Search attendance in groups")
# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/student', methods=['GET'])
def index_student():
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

    if request.method == 'POST':
        if not form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Student.student_id)))[0][0]
            student_obj = Student(
                student_id=id+1,
                group_id=db.sqlalchemy_session.query(Group.group_id).filter(Group.group_name == form.student_group.data),
                student_university=form.student_university.data,
                student_faculty=form.student_faculty.data,
                student_group=form.student_group.data,
                student_name=form.student_name.data)

            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()
            AttendanceForm.reload_students()

            return redirect(url_for('index_student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = StudentForm()

    if request.method == 'GET':

        student_id = request.args.get('student_id')
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
            # find student
            student = db.sqlalchemy_session.query(Student).filter(Student.student_id == form.student_id.data).one()

            # update fields from form data
            student.student_id = student.student_id
            student.group_id = db.sqlalchemy_session.query(Group.group_id).filter(Group.group_name == form.student_group.data)
            student.student_university = form.student_university.data
            student.student_faculty = form.student_faculty.data
            student.student_group = form.student_group.data
            student.student_name = form.student_name.data

            db.sqlalchemy_session.commit()
            AttendanceForm.reload_students()

            return redirect(url_for('index_student'))


@app.route('/delete_student')
def delete_student():
    student_id = request.args.get('student_id')


    result = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()
    result.student_date_expelled = date.today()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()
    AttendanceForm.reload_students()

    return redirect(url_for('index_student'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# GROUP ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/group', methods=['GET'])
def index_group():

    group = db.sqlalchemy_session.query(Group).all()

    return render_template('group.html', groups=group)


@app.route('/new_group', methods=['GET', 'POST'])
def new_group():
    form = GroupForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('group_form.html', form=form, form_name="New group",
                                   action="new_group")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Group.group_id)))[0][0]
            group_obj = Group(
                group_id = id + 1,
                group_name=form.group_name.data)

            db.sqlalchemy_session.add(group_obj)
            db.sqlalchemy_session.commit()
            StudentForm.reload_groups()
            DisciplineForm.reload_groups()
            SearchForm.reload_groups()

            return redirect(url_for('index_group'))

    return render_template('group_form.html', form=form, form_name="New group", action="new_group")


@app.route('/edit_group', methods=['GET', 'POST'])
def edit_group():
    form = GroupForm()

    if request.method == 'GET':

        group_id = request.args.get('group_id')

        group = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()

        # fill form and send to group
        form.group_id.data = group.group_id
        form.group_name.data = group.group_name

        return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")

    else:

        if not form.validate():
            return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")
        else:

            # find group
            group = db.sqlalchemy_session.query(Group).filter(Group.group_id == form.group_id.data).one()

            # update fields from form data
            group.group_id = form.group_id.data
            group.group_name = form.group_name.data

            db.sqlalchemy_session.commit()
            StudentForm.reload_groups()
            DisciplineForm.reload_groups()
            SearchForm.reload_groups()

            return redirect(url_for('index_group'))


@app.route('/delete_group')
def delete_group():
    group_id = request.args.get('group_id')



    result = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()
    result.group_date_expelled = date.today()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()
    StudentForm.reload_groups()
    DisciplineForm.reload_groups()
    SearchForm.reload_groups()

    return redirect(url_for('index_group'))



# END group ORIENTED QUERIES -----------------------------------------------------------------------------------

# discipline ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/discipline', methods=['GET'])
def index_discipline():

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

    if request.method == 'POST':
        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Discipline.discipline_id)))[0][0]
            discipline_obj = Discipline(
                discipline_id = id + 1,
                group_id=db.sqlalchemy_session.query(Group.group_id).filter(Group.group_name==form.discipline_name.data),
                discipline_group=form.discipline_group.data,
                discipline_name=form.discipline_name.data)

            db.sqlalchemy_session.add(discipline_obj)
            db.sqlalchemy_session.commit()
            AttendanceForm.reload_disciplines()
            ScheduleForm.reload_disciplines()

            return redirect(url_for('index_discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")


@app.route('/edit_discipline', methods=['GET', 'POST'])
def edit_discipline():
    form = DisciplineForm()

    if request.method == 'GET':

        discipline_id = request.args.get('discipline_id')
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
            # find discipline
            discipline = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == form.discipline_id.data).one()

            # update fields from form data
            discipline.discipline_id = form.discipline_id.data
            discipline.discipline_group = form.discipline_group.data
            discipline.discipline_name = form.discipline_name.data

            db.sqlalchemy_session.commit()
            AttendanceForm.reload_disciplines()
            ScheduleForm.reload_disciplines()
            return redirect(url_for('index_discipline'))


@app.route('/delete_discipline')
def delete_discipline():
    discipline_id = request.args.get('discipline_id')


    result = db.sqlalchemy_session.query(Discipline).filter(Discipline.discipline_id == discipline_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()
    AttendanceForm.reload_disciplines()
    ScheduleForm.reload_disciplines()

    return redirect(url_for('index_discipline'))


# END discipline ORIENTED QUERIES ----------------------------------------------------------------------------
# SCHEDULE ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/schedule', methods=['GET'])
def index_schedule():

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Schedule).all()
    else:
        result = db.sqlalchemy_session.query(Schedule).all()
        deleted = False

    return render_template('schedule.html', schedules=result, deleted=deleted)


@app.route('/new_schedule', methods=['GET', 'POST'])
def new_schedule():
    form = ScheduleForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('schedule_form.html', form=form, form_name="New schedule", action="new_schedule")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Schedule.class_id)))[0][0]
            schedule_obj = Schedule(
                class_id=id + 1,
                discipline_id=db.sqlalchemy_session.query(Discipline.discipline_id).filter(Discipline.discipline_name==form.discipline_name.data),
                discipline_name=form.discipline_name.data,
                lecture_hall=form.lecture_hall.data,
                class_date=form.class_date.data)
            db.sqlalchemy_session.add(schedule_obj)
            db.sqlalchemy_session.commit()
            # AttendanceForm.reload_dates()

            return redirect(url_for('index_schedule'))

    return render_template('schedule_form.html', form=form, form_name="New schedule", action="new_schedule")


@app.route('/edit_schedule', methods=['GET', 'POST'])
def edit_schedule():
    form = ScheduleForm()

    if request.method == 'GET':

        class_id = request.args.get('class_id')
        schedule = db.sqlalchemy_session.query(Schedule).filter(Schedule.class_id == class_id).one()

        # fill form and send to schedule
        form.class_id.data = schedule.class_id
        form.discipline_id.data = schedule.discipline_id
        form.lecture_hall.data = schedule.lecture_hall
        form.class_date.data = schedule.class_date

        return render_template('schedule_form.html', form=form, form_name="Edit schedule", action="edit_schedule")

    else:

        if not form.validate():
            return render_template('schedule_form.html', form=form, form_name="Edit schedule", action="edit_schedule")
        else:
            # find schedule
            schedule = db.sqlalchemy_session.query(Schedule).filter(Schedule.class_id == form.class_id.data).one()

            # update fields from form data
            schedule.class_id = form.class_id.data
            schedule.discipline_id = form.discipline_id.data
            schedule.lecture_hall = form.lecture_hall.data
            schedule.class_date = form.class_date.data

            db.sqlalchemy_session.commit()
            # AttendanceForm.reload_dates()

            return redirect(url_for('index_schedule'))


@app.route('/delete_schedule')
def delete_schedule():
    class_id = request.args.get('class_id')


    result = db.sqlalchemy_session.query(Schedule).filter(Schedule.class_id == class_id).one()
    # result.student_date_expelled = date.today() TODO delete this if acceptable

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()
    # AttendanceForm.reload_dates()

    return redirect(url_for('index_schedule'))


# END SCHEDULE ORIENTED QUERIES -----------------------------------------------------------------------------------
# ATTENDANCE ORIENTED QUERIES -----------------------------------------------------------------------------------


@app.route('/attendance', methods=['GET'])
def index_attendance():

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Attendance).all()
    else:
        result = db.sqlalchemy_session.query(Attendance).all()
        deleted = False

    return render_template('attendance.html', attendances=result, deleted=deleted)


@app.route('/new_attendance', methods=['GET', 'POST'])
def new_attendance():
    form = AttendanceForm()
    print(form.discipline_name.data)
    if request.method == 'POST':
        if not form.validate():
            return render_template('attendance_form.html', form=form, form_name="New attendance", action="new_attendance")
        else:
            id = list(db.sqlalchemy_session.query(func.max(Attendance.attendance_id)))[0][0]
            attendance_obj = Attendance(
                attendance_id=id+1,
                student_id=db.sqlalchemy_session.query(Student.student_id).filter(Student.student_name==form.student_name.data),
                student_name=form.student_name.data,
                class_id=db.sqlalchemy_session.query(Schedule.class_id).filter(and_(Schedule.discipline_name==form.discipline_name.data,Schedule.class_date==form.class_date.data )),
                discipline_name=form.discipline_name.data,
                class_date=form.class_date.data,
                attended=form.attended.data)

            db.sqlalchemy_session.add(attendance_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_attendance'))

    return render_template('attendance_form.html', form=form, form_name="New attendance", action="new_attendance")


@app.route('/edit_attendance', methods=['GET', 'POST'])
def edit_attendance():
    form = AttendanceForm()

    if request.method == 'GET':

        attendance_id = request.args.get('attendance_id')

        attendance = db.sqlalchemy_session.query(Attendance).filter(Attendance.attendance_id == attendance_id).one()

        # fill form and send to attendance
        form.attendance_id.data = attendance.attendance_id
        form.student_id.data = attendance.student_id
        form.student_name.data = attendance.student_name
        form.class_id.data = attendance.class_id
        form.discipline_name.data = attendance.discipline_name
        form.class_date.data = attendance.class_date
        form.attended.data = attendance.attended

        return render_template('attendance_form.html', form=form, form_name="Edit attendance (change only check!)", action="edit_attendance")

    else:

        if not form.validate():
            return render_template('attendance_form.html', form=form, form_name="Edit attendance (change only check!)", action="edit_attendance")
        else:

            # find attendance
            attendance = db.sqlalchemy_session.query(Attendance).filter(Attendance.attendance_id == form.attendance_id.data).one()

            # update fields from form data
            attendance.attendance_id = form.attendance_id.data,
            attendance.student_id = form.student_id.data,
            attendance.student_name = form.student_name.data,
            attendance.class_id = form.class_id.data,
            attendance.discipline_name = form.discipline_name.data,
            attendance.class_date = form.class_date.data,
            attendance.attended = form.attended.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_attendance'))


@app.route('/delete_attendance')
def delete_attendance():
    attendance_id = request.args.get('attendance_id')


    result = db.sqlalchemy_session.query(Attendance).filter(Attendance.attendance_id == attendance_id).one()
    # result.student_date_expelled = date.today() TODO delete this if acceptable

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_attendance'))


# END ATTENDANCE ORIENTED QUERIES -----------------------------------------------------------------------------------
# HOUSE ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/house', methods=['GET'])
def index_house():

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


    result = db.sqlalchemy_session.query(House).filter(House.house_id == house_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_house'))


# END HOUSE ORIENTED QUERIES ----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
