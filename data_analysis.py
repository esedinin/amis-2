import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from source.dao.orm.entities import *
from sqlalchemy import func, not_
import os
from connection import db


student_id = []
discipline_id = []
student_attended = []
student_skipped = []
attended_percent = []

result = db.sqlalchemy_session.query(Student.student_id, Discipline.discipline_id, func.count(Attendance.student_id).filter(Attendance.attended).label("student_attended"),\
                                     func.count(Attendance.student_id).filter(not_(Attendance.attended)).label("student_skipped"))\
                                    .join(Attendance, Attendance.student_id == Student.student_id)\
                                    .join(Discipline, Discipline.discipline_group == Student.student_group).group_by(Student.student_id, Discipline.discipline_id).all()
for row in result:
    student_id.append(row.student_id)
    discipline_id.append(row.discipline_id)
    student_attended.append(row.student_attended)
    student_skipped.append(row.student_skipped)
    attended_percent.append(row.student_attended / (row.student_attended + row.student_skipped))
# print('-----------------------------------------------')
# print(len(student_id), student_id)
# print(len(discipline_id), discipline_id)
# print(len(student_attended), student_attended)
# print(len(student_skipped), student_skipped)
# print(len(attended_percent), attended_percent)
# print('-----------------------------------------------')
X = pd.DataFrame(list(zip(student_id, discipline_id, attended_percent)), # minus attended and skipped
                     columns=['student_id', 'discipline_id', 'attended_percent'])

y = pd.DataFrame(attended_percent)
# print('X_new', X)
# print('Y_new', y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

regressor = RandomForestRegressor(n_estimators=200, random_state=0)
regressor.fit(X_train, np.ravel(y_train))
y_pred = regressor.predict(X_test)

# print('y_pred = ', y_pred)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

filename = 'finalized_model.pkl'
pickle.dump(regressor, open(filename, 'wb'))

# some time later...

# load the model from disk
def predict():
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.score(X_test, y_test)
    return result
