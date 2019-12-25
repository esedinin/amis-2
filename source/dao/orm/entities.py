from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, MetaData, Table
from sqlalchemy.orm import relationship


Base = declarative_base()


class Group(Base):
    __tablename__ = 'Group'

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(255), nullable=False, index=True, unique=True)

    students = relationship("Student")
    disciplines = relationship("Discipline")


class Student(Base):
    __tablename__ = 'Student'

    student_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('Group.group_id'))
    student_university = Column(String(255), nullable=False)
    student_faculty = Column(String(255), nullable=False)
    student_name = Column(String(255), nullable=False, index=True, unique=True)
    house_id = Column(Integer, nullable=True)
    student_group = Column(String(255), nullable=False)

    attendances = relationship("Attendance")


class Discipline(Base):
    __tablename__ = 'Discipline'

    discipline_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('Group.group_id'))
    discipline_name = Column(String(255), nullable=False, index=True, unique=True)
    discipline_group = Column(String(255), nullable=False)

    schedules = relationship("Schedule")


class Schedule(Base):
    __tablename__ = 'Schedule'

    class_id = Column(Integer, primary_key=True)
    discipline_id = Column(Integer, ForeignKey('Discipline.discipline_id'), nullable=False)
    discipline_name = Column(String(255), nullable=False)
    lecture_hall = Column(String(255), nullable=True)
    class_date = Column(Date, nullable=False)

    attendances = relationship("Attendance")


class Attendance(Base):
    __tablename__ = 'Attendance'

    attendance_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.student_id'))
    student_name = Column(String(255), nullable=False)
    class_id = Column(Integer, ForeignKey('Schedule.class_id'))
    discipline_name = Column(String(255), nullable=False)
    class_date = Column(Date, nullable=False)
    attended = Column(Boolean, nullable=False)


class House(Base):
    __tablename__ = 'House'

    house_id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    floor_count = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


if __name__ == '__main__':
    from source.dao.db import PostgresDb

    db = PostgresDb()
    # Base.metadata.drop_all(db.sqlalchemy_engine)
    # Base.metadata.create_all(db.sqlalchemy_engine)
    print("Entities running")
    # simple query test
    q1 = db.sqlalchemy_session.query(Group).all()
    q2 = db.sqlalchemy_session.query(Student).all()
    q3 = db.sqlalchemy_session.query(Discipline).all()

    print()