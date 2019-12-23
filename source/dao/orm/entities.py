from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'Student'

    student_id = Column(Integer, primary_key=True)
    student_university = Column(String(255), nullable=False)
    student_faculty = Column(String(255), nullable=False)
    student_group = Column(String(255), ForeignKey('Group.group_name'), nullable=False, unique=True)
    student_name = Column(String(255), nullable=False)
    house_id = Column(Integer, nullable=True)

class Group(Base):
    __tablename__ = 'Group'

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(255), nullable=False, unique=True)
    student = relationship("Student", back_populates="Group")


class Discipline(Base):
    __tablename__ = 'Discipline'

    discipline_id = Column(Integer, primary_key=True)
    discipline_name = Column(String(255), nullable=False)
    discipline_group = Column(String(255), nullable=False)


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
    # simple query test
    q1 = db.sqlalchemy_session.query(Group).all()
    q2 = db.sqlalchemy_session.query(Student).all()
    q3 = db.sqlalchemy_session.query(Discipline).all()

    # a = db.sqlalchemy_session.query(Student).join(Group).join(Discipline).all()
    print()
