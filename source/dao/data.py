import os

username = 'xyikxvguklthze'
password = '74e3a7a712173572b976791f1f1e607cc29838d23e1572c37e3a2881f499729e'
host = 'ec2-174-129-24-148.compute-1.amazonaws.com'
port = '5432'
database = 'postgres'
DATABASE_URI = os.getenv("DATABASE_URL",
                         'postgres://xyikxvguklthze:74e3a7a712173572b976791f1f1e607cc29838d23e1572c37e3a2881f499729e@ec2-174-129-24-148.compute-1.amazonaws.com:5432/d1gnq35nqlip83'.format(password, host, port, database))
