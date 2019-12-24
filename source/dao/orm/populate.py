import datetime

from source.dao.orm.entities import *
from source.dao.db import PostgresDb

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

session.query(Attendance).delete()
session.query(Schedule).delete()
session.query(Discipline).delete()
session.query(Student).delete()
session.query(House).delete()
session.query(Group).delete()

Sedinin = Student(student_id=1, group_id=1, student_university='KPI', student_faculty='FPM', student_group='KM-62', student_name='Sedinin Yehor', house_id=None)

km_62 = Group(group_id=1, group_name='KM-62')


# pop = genre(id=1, name='pop', psychotype='gipertim')
# indie = genre(id=2, name='indie', psychotype='emotive')
# rock = genre(id=3, name='rock', psychotype='isteroid')
# romans = genre(id=4, name='romans', psychotype='disturbing')
# classic = genre(id=5, name='classic', psychotype='PSYCHASTENOID')
# blues = genre(id=6, name='blues', psychotype='emotive')
# jazz = genre(id=7, name='jazz', psychotype='gipertim')
#
# Elzy = performer(id=1, name='Okean Elzy')
# Hardkiss = performer(id=2, name='The Hardkiss')
# Babkin = performer(id=3, name='Serhii Babkin')
# Zemfira = performer(id=4, name='Zemfira')
# Jackson = performer(id=5, name='Michael Jackson')
#
# no_album1 = album(id=0, title='Blues', performer_id=4)
# Zemlya = album(id=1, title='Zemlya', performer_id=1)
# Closer = album(id=2, title='Closer', performer_id=2)
# Muzasfera = album(id=3, title='Muzasfera', performer_id=3)
# no_album2 = album(id=4, title='Smooth Criminal', performer_id=5)
#
# Prirva = melody(id=1, title='Prirva', singer='The Hardkiss', release_date=datetime.date(2016, 4, 19), melody_genre=4,album_id=2)
# Blues = melody(id=2, title='Blues', singer='Zemfira', release_date=datetime.date(2009, 12, 30), melody_genre=6,album_id=0)
# Criminal = melody(id=3, title='Smooth Criminal', singer='Michael Jackson', release_date=datetime.date(1997, 11, 5), melody_genre=1,album_id=4)
#
# atam1912 = wish(id=1, student_id=1, wish_date=datetime.date(2019, 12, 19), wish_performer='Zemfira', wish_melody=2,wish_genre=6)
# kovt1912 = wish(id=2, student_id=4, wish_date=datetime.date(2019, 12, 19), wish_performer='', wish_melody=3,wish_genre=1)
# paly1812 = wish(id=3, student_id=5, wish_date=datetime.date(2019, 12, 18), wish_performer='', wish_melody=2,wish_genre=6)
# kube1612 = wish(id=4, student_id=7, wish_date=datetime.date(2019, 12, 16), wish_performer='', wish_melody=2,wish_genre=6)
session.add_all([Sedinin, km_62])

session.commit()
