from source.dao.orm.entities import *
from source.dao.db import PostgresDb
import datetime

db = PostgresDb()

Base.metadata.drop_all(db.sqlalchemy_engine)
Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

# TODO deleting all db after every deploy is not really good

session.query(Attendance).delete()
session.query(Schedule).delete()
session.query(Discipline).delete()
session.query(Student).delete()
session.query(House).delete()
session.query(Group).delete()


km_62 = Group(group_id=1, group_name='KM-62')
km_61 = Group(group_id=2, group_name='KM-61')
kv_61 = Group(group_id=3, group_name='KV-61')
kp_73 = Group(group_id=4, group_name='KP-73')

Sedinin = Student(student_id=1, group_id=1, student_university='KPI', student_faculty='FPM', student_group="KM-62", student_name='Sedinin Yehor', house_id=None)
Pavlov = Student(student_id=2, group_id=1, student_university='KPI', student_faculty='FPM', student_group="KM-62", student_name='Pavlov Pavlo', house_id=None)
Ivanov = Student(student_id=3, group_id=1, student_university='KPI', student_faculty='FPM', student_group="KM-62", student_name='Ivanov Ivan', house_id=None)
Antonov = Student(student_id=4, group_id=2, student_university='KPI', student_faculty='FPM', student_group="KM-61", student_name='Antonov Anton', house_id=None)
Testov = Student(student_id=5, group_id=3, student_university='KPI', student_faculty='FPM', student_group="KV-61", student_name='Testov Test', house_id=None)
Vovov = Student(student_id=6, group_id=4, student_university='NAU', student_faculty='HMM', student_group="KP-73", student_name='Vovov Vova', house_id=None)

Math = Discipline(discipline_id=1, discipline_name='Math', discipline_group='KM-62')
DB = Discipline(discipline_id=2, discipline_name='DB', discipline_group='KM-61')
AI = Discipline(discipline_id=3, discipline_name='AI', discipline_group='KV-61')
DS = Discipline(discipline_id=4, discipline_name='DS', discipline_group='KP-73')

Math1 = Schedule(class_id=1, discipline_id=1, class_date=datetime.date(2019, 12, 25), lecture_hall='209-19')
Math2 = Schedule(class_id=2, discipline_id=1, class_date=datetime.date(2019, 12, 29), lecture_hall='209-19')
DB1 = Schedule(class_id=3, discipline_id=2, class_date=datetime.date(2019, 12, 25), lecture_hall='105-07')

Math1Sedinin = Attendance(attendance_id=1, class_id=1, student_id=1, attended=True)
Math1Pavlov = Attendance(attendance_id=2, class_id=1, student_id=2, attended=True)
Math1Ivanov = Attendance(attendance_id=3, class_id=1, student_id=3, attended=False)
Math2Sedinin = Attendance(attendance_id=4, class_id=2, student_id=1, attended=False)
Math2Pavlov = Attendance(attendance_id=5, class_id=2, student_id=2, attended=True)
Math2Ivanov = Attendance(attendance_id=6, class_id=2, student_id=3, attended=False)
DB1Antonov = Attendance(attendance_id=7, class_id=3, student_id=4, attended=True)

session.add_all([km_61, km_62, kv_61, kp_73, Sedinin, Pavlov, Ivanov, Antonov, Testov, Vovov, Math, DB, AI, DS, Math1,
                 Math2, DB1, Math1Sedinin, Math1Pavlov, Math1Ivanov, Math2Sedinin, Math2Pavlov, Math2Ivanov, DB1Antonov])

session.commit()
